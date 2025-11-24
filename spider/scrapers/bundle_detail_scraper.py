from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup
from requests import Session, exceptions

logger = logging.getLogger(__name__)


@dataclass
class BundleDetails:
    """Detalles de un bundle extraídos del JSON, sin imágenes."""
    price_tiers: List[Dict[str, Any]]
    book_list: List[Dict[str, Any]]  # Sin campo 'image'
    msrp_total: Optional[float]
    raw_html: Optional[str] = None  # HTML raw del bundle


class BundleDetailScraper:
    """
    Scraper que extrae detalles de bundles desde el JSON embebido en la página.
    Solo extrae datos del JSON (price_tiers, book_list, msrp_total), NO extrae imágenes.
    """
    BASE_URL = 'https://www.humblebundle.com'

    def __init__(self, session: Session | None = None) -> None:
        """
        Inicializa el scraper de detalles de bundles.
        
        Args:
            session: Sesión de requests a usar. Si es None, se crea una nueva.
        """
        self.session = session or Session()

    def fetch_bundle_details(self, product_path: str | None) -> Optional[BundleDetails]:
        """
        Obtiene los detalles de un bundle desde su página.
        
        Extrae información del JSON embebido (webpack-bundle-page-data) sobre
        precios, lista de libros y MSRP total. NO extrae imágenes.
        
        Args:
            product_path: Ruta o URL del producto. Puede ser relativa o absoluta.
            
        Returns:
            BundleDetails con la información extraída o None si hay un error.
        """
        if not product_path:
            return None
        
        url = product_path if product_path.startswith('http') else f'{self.BASE_URL}{product_path}'
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
        except exceptions.RequestException as exc:
            logger.warning('No se pudo obtener detalle del bundle %s: %s', product_path, exc)
            return None

        # Guardar HTML raw para tests
        raw_html = response.text
        
        soup = BeautifulSoup(response.text, 'html.parser')
        script = soup.find('script', id='webpack-bundle-page-data', type='application/json')
        if not script or not script.string:
            logger.warning('Script webpack-bundle-page-data no encontrado para %s', product_path)
            return None

        try:
            data = json.loads(script.string)
            bundle_data = data['bundleData']
        except (json.JSONDecodeError, KeyError) as exc:
            logger.warning('JSON inválido en detalle %s: %s', product_path, exc)
            return None
        
        tier_pricing = bundle_data.get('tier_pricing_data', {})
        tier_display = bundle_data.get('tier_display_data', {})
        tier_items = bundle_data.get('tier_item_data', {})
        
        price_tiers = self._extract_price_tiers(tier_pricing, tier_display)
        book_list = self._extract_book_list(tier_items, tier_display)
        
        basic_data = bundle_data.get('basic_data', {})
        msrp_total = self._safe_amount(basic_data.get('msrp|money'))
        
        return BundleDetails(
            price_tiers=price_tiers,
            book_list=book_list,
            msrp_total=msrp_total,
            raw_html=raw_html,
        )

    @staticmethod
    def _extract_price_tiers(pricing, display) -> List[Dict[str, Any]]:
        """
        Extrae los tiers de precios del JSON.
        
        Args:
            pricing: Diccionario con información de precios por tier
            display: Diccionario con información de visualización de los tiers
            
        Returns:
            Lista de diccionarios con información de cada tier
        """
        tiers: List[Dict[str, Any]] = []
        for identifier, info in pricing.items():
            tiers.append(
                {
                    'identifier': identifier,
                    'price': info.get('price|money'),
                    'average_purchase_price': info.get('average_purchase_price|money'),
                    'is_initial': info.get('is_initial_tier'),
                    'header': display.get(identifier, {}).get('header'),
                    'items': display.get(identifier, {}).get('tier_item_machine_names', []),
                }
            )
        return tiers

    def _extract_book_list(self, tier_items, display) -> List[Dict[str, Any]]:
        """
        Extrae la lista de libros del bundle desde los datos del JSON.
        
        Construye la lista de libros con sus metadatos, precios y tiers.
        NO incluye imágenes.
        
        Args:
            tier_items: Diccionario con información de los items por tier
            display: Diccionario con información de visualización de los tiers
                
        Returns:
            Lista de diccionarios, cada uno representando un libro con sus
            metadatos (machine_name, title, msrp, preview, content_type, tiers).
        """
        membership: Dict[str, List[str]] = {}
        for tier_id, data in display.items():
            for machine in data.get('tier_item_machine_names', []):
                membership.setdefault(machine, []).append(tier_id)

        books: List[Dict[str, Any]] = []
        for machine_name, info in tier_items.items():
            books.append(
                {
                    'machine_name': machine_name,
                    'title': info.get('human_name'),
                    'msrp': BundleDetailScraper._safe_amount(info.get('msrp_price')),
                    'preview': info.get('book_preview'),
                    # NO incluir 'image'
                    'content_type': info.get('item_content_type'),
                    'tiers': membership.get(machine_name, []),
                }
            )
        return books

    @staticmethod
    def _safe_amount(value: Optional[Dict[str, Any]]) -> Optional[float]:
        """
        Extrae el valor numérico de un objeto de dinero del JSON.
        
        Args:
            value: Diccionario con información de dinero (ej: {'amount': 29.99, 'currency': 'USD'})
            
        Returns:
            Valor numérico como float o None si no se puede extraer
        """
        if not value:
            return None
        amount = value.get('amount')
        if isinstance(amount, (int, float)):
            return float(amount)
        try:
            return float(amount)
        except (TypeError, ValueError):
            return None

