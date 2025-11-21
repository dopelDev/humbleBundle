from __future__ import annotations

import json
import logging
from typing import Dict, List

import pandas as pd
from bs4 import BeautifulSoup
from pydantic import ValidationError
from requests import Session, exceptions

from ..scrapers.image_scraper import ImageUrlScraper
from ..schemas.bundle import BundleRecord
from ..utils.transformers import (
    absolute_url,
    compute_duration_days,
    compute_is_active,
    normalize_columns,
    serialize_list,
    safe_float,
)
from .errors import HumbleSpiderError

logger = logging.getLogger(__name__)


class HumbleSpider:
    """
    Obtiene los bundles publicados en Humble Bundle Books y los serializa a BundleRecord.
    """

    URL = 'https://www.humblebundle.com/books'
    SCRIPT_ID = 'landingPage-json-data'
    JSON_COLUMNS = ('hero_highlights', 'hover_highlights', 'highlights')
    DATETIME_COLUMNS = ('start_date|datetime', 'end_date|datetime')
    TEXT_COLUMNS = (
        'machine_name',
        'marketing_blurb',
        'hover_title',
        'product_url',
        'category',
        'author',
        'tile_name',
        'tile_short_name',
        'tile_stamp',
        'short_marketing_blurb',
    )

    def __init__(self, session: Session | None = None) -> None:
        self.session = session or Session()
        self.image_scraper = ImageUrlScraper(self.session)

    def fetch_bundles(self) -> List[BundleRecord]:
        payload = self._fetch_raw_payload()
        products = self._extract_products(payload)
        frame = self._normalize_products(products)
        return self._to_records(frame)

    def _fetch_raw_payload(self) -> Dict:
        try:
            response = self.session.get(self.URL, timeout=30)
            response.raise_for_status()
        except exceptions.RequestException as exc:
            logger.exception('Error consultando %s', self.URL)
            raise HumbleSpiderError('No se pudo obtener la página de Humble Bundle') from exc

        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.select_one(f'script#{self.SCRIPT_ID}')
        if not script_tag or not script_tag.string:
            raise HumbleSpiderError('No se encontró el script con los datos esperados')
        return json.loads(script_tag.string)

    def _extract_products(self, payload: Dict) -> List[Dict]:
        try:
            return payload['data']['books']['mosaic'][0]['products']
        except (KeyError, IndexError, TypeError) as exc:
            raise HumbleSpiderError('Estructura JSON inesperada al obtener productos') from exc

    def _normalize_products(self, products: List[Dict]) -> pd.DataFrame:
        frame = pd.json_normalize(products)
        if frame.empty:
            return frame

        frame.replace('', None, inplace=True)
        frame.dropna(axis=1, how='all', inplace=True)

        for column in self.DATETIME_COLUMNS:
            if column in frame.columns:
                frame[column] = pd.to_datetime(frame[column], errors='coerce', utc=True)

        for column in self.JSON_COLUMNS:
            if column in frame.columns:
                frame[column] = frame[column].apply(serialize_list)

        normalize_columns(frame, self.TEXT_COLUMNS)

        if 'product_url' in frame.columns:
            frame['product_url'] = frame['product_url'].apply(absolute_url)

        if 'bundles_sold|decimal' in frame.columns:
            frame['bundles_sold|decimal'] = frame['bundles_sold|decimal'].apply(safe_float)

        frame['duration_days'] = frame.apply(
            lambda row: compute_duration_days(row.get('start_date|datetime'), row.get('end_date|datetime')),
            axis=1,
        )
        frame['is_active'] = frame.apply(
            lambda row: compute_is_active(row.get('start_date|datetime'), row.get('end_date|datetime')),
            axis=1,
        )

        return frame

    def _to_records(self, frame: pd.DataFrame) -> List[BundleRecord]:
        if frame.empty:
            return []
        records: List[BundleRecord] = []
        discarded = 0
        for item in frame.to_dict(orient='records'):
            machine_name = item.get('machine_name')
            detail = self.image_scraper.fetch_detail(item.get('product_url'), machine_name=machine_name)
            if detail:
                item['price_tiers'] = detail.price_tiers
                item['book_list'] = detail.book_list
                item['featured_image'] = detail.featured_image
                item['msrp_total'] = detail.msrp_total
                item['raw_html'] = detail.raw_html  # Guardar HTML raw para tests
                # Guardar URLs scrapeadas en el item para persistirlas después
                item['_scraped_image_urls'] = detail.scraped_image_urls or []
            try:
                record = BundleRecord.model_validate(item)
                # Guardar las URLs scrapeadas como atributo del record (no en el modelo)
                if detail and detail.scraped_image_urls:
                    setattr(record, '_scraped_image_urls', detail.scraped_image_urls)
            except ValidationError as exc:
                discarded += 1
                logger.warning('Registro descartado %s: %s', item.get('machine_name'), exc)
                continue
            records.append(record)
        if discarded:
            logger.info('Descartados %s registros por validación', discarded)
        return records

