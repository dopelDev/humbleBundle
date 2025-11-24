from __future__ import annotations

import hashlib
import json
import logging
from typing import Dict, List, Optional

import pandas as pd
from bs4 import BeautifulSoup
from pydantic import ValidationError
from requests import Session, exceptions

from ..scrapers.bundle_detail_scraper import BundleDetailScraper
from ..schemas.bundle import BundleRecord
from ..schemas.raw_data import LandingPageRawDataRecord
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
        'tile_logo',
    )

    def __init__(self, session: Session | None = None) -> None:
        """
        Inicializa el spider de Humble Bundle.

        Args:
            session: Sesión de requests a usar. Si es None, se crea una nueva.
        """
        self.session = session or Session()
        self.detail_scraper = BundleDetailScraper(self.session)
        self._last_raw_payload: Optional[Dict] = None

    def fetch_bundles(self) -> List[BundleRecord]:
        """
        Obtiene y procesa todos los bundles disponibles de Humble Bundle.

        Realiza el scraping de la página de Humble Bundle, extrae los datos
        de los productos, los normaliza y los convierte en registros validados.

        Returns:
            Lista de BundleRecord con los bundles obtenidos y validados.

        Raises:
            HumbleSpiderError: Si hay un error al obtener o procesar los datos.
        """
        payload = self._fetch_raw_payload()
        self._last_raw_payload = payload
        products = self._extract_products(payload)
        frame = self._normalize_products(products)
        return self._to_records(frame)

    def get_raw_data_record(self) -> Optional[LandingPageRawDataRecord]:
        """
        Obtiene el raw data record del último payload obtenido.

        Crea un LandingPageRawDataRecord con el JSON raw del último
        landingPage-json-data obtenido, incluyendo hash y metadata.

        Returns:
            LandingPageRawDataRecord con el JSON y metadata, o None si
            no se ha obtenido ningún payload aún.
        """
        if not self._last_raw_payload:
            return None

        # Calcular hash del JSON
        json_str = json.dumps(self._last_raw_payload,
                              sort_keys=True, ensure_ascii=False)
        json_hash = hashlib.sha256(json_str.encode('utf-8')).hexdigest()

        return LandingPageRawDataRecord(
            json_data=self._last_raw_payload,
            source_url=self.URL,
            json_hash=json_hash,
            json_version=None,  # Se puede agregar lógica para detectar versión si es necesario
        )

    def _fetch_raw_payload(self) -> Dict:
        """
        Obtiene el payload JSON crudo desde la página de Humble Bundle.

        Realiza una petición HTTP a la página de libros y extrae el JSON
        embebido en el script con id 'landingPage-json-data'.

        Returns:
            Diccionario con los datos JSON extraídos de la página.

        Raises:
            HumbleSpiderError: Si no se puede obtener la página o el script
                con los datos no se encuentra.
        """
        try:
            response = self.session.get(self.URL, timeout=30)
            response.raise_for_status()
        except exceptions.RequestException as exc:
            logger.exception('Error consultando %s', self.URL)
            raise HumbleSpiderError(
                'No se pudo obtener la página de Humble Bundle') from exc

        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.select_one(f'script#{self.SCRIPT_ID}')
        if not script_tag or not script_tag.string:
            raise HumbleSpiderError(
                'No se encontró el script con los datos esperados')
        return json.loads(script_tag.string)

    def _extract_products(self, payload: Dict) -> List[Dict]:
        """
        Extrae la lista de productos del payload JSON.

        Args:
            payload: Diccionario con los datos JSON obtenidos de la página.

        Returns:
            Lista de diccionarios, cada uno representando un producto/bundle.

        Raises:
            HumbleSpiderError: Si la estructura del JSON no es la esperada.
        """
        try:
            return payload['data']['books']['mosaic'][0]['products']
        except (KeyError, IndexError, TypeError) as exc:
            raise HumbleSpiderError(
                'Estructura JSON inesperada al obtener productos') from exc

    def _normalize_products(self, products: List[Dict]) -> pd.DataFrame:
        """
        Normaliza y transforma los productos en un DataFrame de pandas.

        Realiza las siguientes transformaciones:
        - Convierte listas anidadas a JSON strings
        - Normaliza fechas a datetime UTC
        - Normaliza columnas de texto
        - Convierte URLs relativas a absolutas
        - Calcula duración en días y estado activo

        Args:
            products: Lista de diccionarios con datos de productos.

        Returns:
            DataFrame de pandas con los productos normalizados.
        """
        frame = pd.json_normalize(products)
        if frame.empty:
            return frame

        frame.replace('', None, inplace=True)
        frame.dropna(axis=1, how='all', inplace=True)

        for column in self.DATETIME_COLUMNS:
            if column in frame.columns:
                frame[column] = pd.to_datetime(
                    frame[column], errors='coerce', utc=True)

        for column in self.JSON_COLUMNS:
            if column in frame.columns:
                frame[column] = frame[column].apply(serialize_list)

        normalize_columns(frame, self.TEXT_COLUMNS)

        if 'product_url' in frame.columns:
            frame['product_url'] = frame['product_url'].apply(absolute_url)

        if 'bundles_sold|decimal' in frame.columns:
            frame['bundles_sold|decimal'] = frame['bundles_sold|decimal'].apply(
                safe_float)

        frame['duration_days'] = frame.apply(
            lambda row: compute_duration_days(
                row.get('start_date|datetime'), row.get('end_date|datetime')),
            axis=1,
        )
        frame['is_active'] = frame.apply(
            lambda row: compute_is_active(
                row.get('start_date|datetime'), row.get('end_date|datetime')),
            axis=1,
        )

        return frame

    def _to_records(self, frame: pd.DataFrame) -> List[BundleRecord]:
        """
        Convierte el DataFrame en una lista de BundleRecord validados.

        Para cada producto, obtiene detalles adicionales (precios, libros, imágenes)
        mediante scraping de la página del bundle y valida los datos usando
        el schema BundleRecord.

        Args:
            frame: DataFrame con productos normalizados.

        Returns:
            Lista de BundleRecord validados. Los registros que no pasan la
            validación se descartan y se registra un warning.
        """
        if frame.empty:
            return []
        records: List[BundleRecord] = []
        discarded = 0
        for item in frame.to_dict(orient='records'):
            machine_name = item.get('machine_name')
            detail = self.detail_scraper.fetch_bundle_details(item.get('product_url'))
            if detail:
                item['price_tiers'] = detail.price_tiers
                item['book_list'] = detail.book_list
                item['msrp_total'] = detail.msrp_total
                # Guardar HTML raw para tests
                item['raw_html'] = detail.raw_html
                # tile_logo ya viene del JSON inicial, pero verificar que esté normalizado
                if 'tile_logo' in item and item['tile_logo']:
                    item['tile_logo'] = absolute_url(item['tile_logo'])
                    logger.debug('tile_logo extraído para %s: %s', machine_name, item.get('tile_logo'))
            try:
                record = BundleRecord.model_validate(item)
            except ValidationError as exc:
                discarded += 1
                logger.warning('Registro descartado %s: %s',
                               item.get('machine_name'), exc)
                continue
            records.append(record)
        if discarded:
            logger.info('Descartados %s registros por validación', discarded)
        return records
