from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from requests import Session, exceptions

from ..core.errors import ImageUrlScraperError

logger = logging.getLogger(__name__)


def _normalize_image_url(url: str, base_url: str) -> Optional[str]:
    """
    Normaliza una URL de imagen a su forma absoluta.
    
    Args:
        url: URL relativa o absoluta
        base_url: URL base (ej: https://www.humblebundle.com)
        
    Returns:
        URL absoluta o None si es inválida
    """
    if not url:
        return None
    
    # Si ya es absoluta, retornarla tal cual
    if url.startswith('http://') or url.startswith('https://'):
        return url
    
    # Si empieza con //, agregar protocolo
    if url.startswith('//'):
        return f'https:{url}'
    
    # Si es relativa y empieza con /, construir URL completa directamente
    if url.startswith('/'):
        return f'{base_url}{url}'
    
    # Si no tiene / al inicio y no empieza con images/, agregar /images/
    # Pero solo si no parece ser ya una ruta completa
    url_clean = url.lstrip("/")
    if url_clean.startswith('images/'):
        # Ya tiene images/, no duplicar
        return f'{base_url}/{url_clean}'
    
    # Si parece ser solo un nombre de archivo, agregar /images/
    return f'{base_url}/images/{url_clean}'


def _is_image_url(url: str) -> bool:
    """
    Verifica si una URL parece ser de una imagen.
    
    Comprueba si la URL termina con una extensión de imagen conocida
    (.jpg, .jpeg, .png, .webp, .gif) o contiene 'imgix' en la URL.
    
    Args:
        url: URL a verificar.
        
    Returns:
        True si la URL parece ser de una imagen, False en caso contrario.
    """
    if not url:
        return False
    url_lower = url.lower()
    return any(url_lower.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']) or 'imgix' in url_lower


def _extract_filename_from_url(url: str) -> Optional[str]:
    """
    Extrae el nombre del archivo de una URL.
    
    Args:
        url: URL de la imagen
        
    Returns:
        Nombre del archivo o None
    """
    if not url:
        return None
    
    try:
        # Intentar parsear la URL
        parsed = urlparse(url)
        path = parsed.path
        # Extraer el nombre del archivo
        filename = Path(path).name
        return filename if filename else None
    except Exception:
        # Si falla, intentar extraer directamente del string
        # Buscar el último segmento después de /
        parts = url.rstrip('/').split('/')
        if parts:
            last_part = parts[-1]
            # Verificar que tenga extensión de imagen
            if any(last_part.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']):
                return last_part
        return None


@dataclass
class BundleDetail:
    price_tiers: List[Dict[str, Any]]
    book_list: List[Dict[str, Any]]
    featured_image: Optional[str]
    msrp_total: Optional[float]
    raw_html: Optional[str] = None  # HTML raw del bundle


class ImageUrlScraper:
    BASE_URL = 'https://www.humblebundle.com'

    def __init__(self, session: Session | None = None) -> None:
        """
        Inicializa el scraper de URLs de imágenes.
        
        Args:
            session: Sesión de requests a usar. Si es None, se crea una nueva.
        """
        self.session = session or Session()

    def fetch_detail(self, product_path: str | None, machine_name: str | None = None) -> Optional[BundleDetail]:
        """
        Obtiene los detalles completos de un bundle desde su página.
        
        Realiza scraping de la página del bundle para extraer información
        sobre precios, lista de libros e imágenes resolviendo las rutas
        encontradas en el HTML.
        
        Args:
            product_path: Ruta o URL del producto. Puede ser relativa o absoluta.
            machine_name: Nombre de máquina del bundle (opcional, no se usa actualmente).
            
        Returns:
            BundleDetail con la información extraída o None si hay un error.
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
        
        # Extraer URLs de imágenes JPG del HTML usando BeautifulSoup
        image_urls_map = self._extract_jpg_urls_from_html_with_info(soup, response.text)
        
        tier_pricing = bundle_data.get('tier_pricing_data', {})
        tier_display = bundle_data.get('tier_display_data', {})
        tier_items = bundle_data.get('tier_item_data', {})
        
        price_tiers = self._extract_price_tiers(tier_pricing, tier_display)
        book_list = self._extract_book_list(tier_items, tier_display, image_urls_map)
        
        basic_data = bundle_data.get('basic_data', {})
        featured_image_url = basic_data.get('logo')
        
        msrp_total = self._safe_amount(basic_data.get('msrp|money'))
        
        # Buscar la URL correcta en el mapeo extraído del HTML
        featured_image = self._resolve_image_url(featured_image_url, image_urls_map)
        
        return BundleDetail(
            price_tiers=price_tiers,
            book_list=book_list,
            featured_image=featured_image,
            msrp_total=msrp_total,
            raw_html=raw_html,
        )

    @staticmethod
    def _extract_price_tiers(pricing, display) -> List[Dict[str, Any]]:
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

    def _extract_book_list(self, tier_items, display, image_urls_map: Dict[str, str] = None) -> List[Dict[str, Any]]:
        """
        Extrae la lista de libros del bundle desde los datos del JSON.
        
        Construye la lista de libros con sus metadatos, precios, imágenes
        y la información de a qué tier pertenece cada libro.
        
        Args:
            tier_items: Diccionario con información de los items por tier.
            display: Diccionario con información de visualización de los tiers.
            image_urls_map: Mapeo de nombres de archivo a URLs absolutas
                extraídas del HTML. Si es None, se usa un diccionario vacío.
                
        Returns:
            Lista de diccionarios, cada uno representando un libro con sus
            metadatos (machine_name, title, msrp, preview, image, content_type, tiers).
        """
        if image_urls_map is None:
            image_urls_map = {}
        
        membership: Dict[str, List[str]] = {}
        for tier_id, data in display.items():
            for machine in data.get('tier_item_machine_names', []):
                membership.setdefault(machine, []).append(tier_id)

        books: List[Dict[str, Any]] = []
        for machine_name, info in tier_items.items():
            image_url = info.get('featured_image') or info.get('preview_image')
            
            # Buscar la URL correcta en el mapeo extraído del HTML
            resolved_image_url = self._resolve_image_url(image_url, image_urls_map)

            books.append(
                {
                    'machine_name': machine_name,
                    'title': info.get('human_name'),
                    'msrp': ImageUrlScraper._safe_amount(info.get('msrp_price')),
                    'preview': info.get('book_preview'),
                    'image': resolved_image_url,
                    'content_type': info.get('item_content_type'),
                    'tiers': membership.get(machine_name, []),
                }
            )
        return books

    @staticmethod
    def _get_absolute_url_from_html(url: str) -> Optional[str]:
        """
        Obtiene la URL absoluta desde el HTML.
        Si ya es absoluta (imgix, cdn, etc.), la retorna tal cual.
        Si es relativa, la normaliza a URL absoluta usando BASE_URL.
        """
        if not url:
            return None
        
        # Si ya es absoluta (http/https), retornarla tal cual (imgix, cdn, etc.)
        if url.startswith('http://') or url.startswith('https://'):
            return url
        
        # Protocolo relativo (//domain.com/path) - convertir a https
        if url.startswith('//'):
            return f'https:{url}'
        
        # URLs relativas - normalizar a URL absoluta
        # Esto incluye URLs como /images/popups/file.jpg o images/popups/file.jpg
        base_url = ImageUrlScraper.BASE_URL
        if url.startswith('/'):
            return f'{base_url}{url}'
        
        # Si no tiene / al inicio
        return f'{base_url}/{url.lstrip("/")}'
    
    @staticmethod
    def _extract_jpg_urls_from_html(soup: BeautifulSoup, html_content: str) -> Dict[str, str]:
        """
        Extrae URLs de imágenes JPG del HTML usando BeautifulSoup (método legacy).
        Mantenido para compatibilidad.
        """
        return ImageUrlScraper._extract_jpg_urls_from_html_with_info(soup, html_content)
    
    @staticmethod
    def _extract_jpg_urls_from_html_with_info(soup: BeautifulSoup, html_content: str) -> Dict[str, str]:
        """
        Extrae URLs de imágenes JPG del HTML usando BeautifulSoup.
        Retorna un mapeo filename -> URL absoluta encontrado en el HTML.
        
        Args:
            soup: Objeto BeautifulSoup del HTML parseado
            html_content: Contenido HTML como string
            
        Returns:
            Diccionario mapeo para localizar imágenes por filename.
        """
        image_urls_map: Dict[str, str] = {}
        seen_urls: set[str] = set()
        
        # 1. Buscar en etiquetas <img> - SOLO URLs absolutas
        img_tags = soup.find_all('img')
        for img in img_tags:
            for attr in ['src', 'data-src', 'data-lazy-src', 'data-original', 'srcset']:
                url = img.get(attr)
                if url:
                    if attr == 'srcset':
                        # srcset: "url1 1x, url2 2x"
                        urls = [u.strip().split()[0] for u in url.split(',')]
                        for u in urls:
                            absolute_url = ImageUrlScraper._get_absolute_url_from_html(u)
                            if absolute_url and absolute_url not in seen_urls:
                                seen_urls.add(absolute_url)
                                filename = _extract_filename_from_url(absolute_url)
                                if filename:
                                    image_urls_map[filename] = absolute_url
                    else:
                        absolute_url = ImageUrlScraper._get_absolute_url_from_html(url)
                        if absolute_url and absolute_url not in seen_urls:
                            seen_urls.add(absolute_url)
                            filename = _extract_filename_from_url(absolute_url)
                            if filename:
                                image_urls_map[filename] = absolute_url
        
        # 2. Buscar en atributos style (background-image: url(...))
        style_tags = soup.find_all(style=True)
        url_pattern = r'url\(["\']?([^"\'()]+\.(jpg|jpeg|png|webp|gif))["\']?\)'
        for tag in style_tags:
            style = tag.get('style', '')
            matches = re.finditer(url_pattern, style, re.IGNORECASE)
            for match in matches:
                url = match.group(1)
                absolute_url = ImageUrlScraper._get_absolute_url_from_html(url)
                if absolute_url and absolute_url not in seen_urls:
                    seen_urls.add(absolute_url)
                    filename = _extract_filename_from_url(absolute_url)
                    if filename:
                        image_urls_map[filename] = absolute_url
        
        # 3. Buscar en atributos data-image, data-bg, etc.
        data_image_attrs = ['data-image', 'data-bg', 'data-background', 'data-img']
        for attr in data_image_attrs:
            tags = soup.find_all(attrs={attr: True})
            for tag in tags:
                url = tag.get(attr)
                absolute_url = ImageUrlScraper._get_absolute_url_from_html(url)
                if absolute_url and absolute_url not in seen_urls:
                    seen_urls.add(absolute_url)
                    filename = _extract_filename_from_url(absolute_url)
                    if filename:
                        image_urls_map[filename] = absolute_url
        
        # 4. Buscar en el JSON embebido (webpack-bundle-page-data)
        script = soup.find('script', id='webpack-bundle-page-data', type='application/json')
        if script and script.string:
            try:
                data = json.loads(script.string)
                json_urls = ImageUrlScraper._extract_urls_from_json(data)
                for url in json_urls:
                    absolute_url = ImageUrlScraper._get_absolute_url_from_html(url)
                    if absolute_url and absolute_url not in seen_urls:
                        seen_urls.add(absolute_url)
                        filename = _extract_filename_from_url(absolute_url)
                        if filename:
                            image_urls_map[filename] = absolute_url
            except Exception as exc:
                logger.debug(f"Error procesando JSON embebido: {exc}")
        
        # 5. Buscar en el HTML usando regex - TODAS las URLs JPG/JPEG (absolutas y relativas)
        jpg_patterns = [
            # URLs absolutas con extensión JPG/JPEG
            r'(https?://[^"\'<>)\s]+\.(jpg|jpeg)(?:\?[^"\'<>)\s]*)?)',
            # URLs relativas con extensión JPG/JPEG
            r'["\'](/[^"\'<>)\s]+\.(jpg|jpeg)(?:\?[^"\'<>)\s]*)?)["\']',
            r'["\'](images/[^"\'<>)\s]+\.(jpg|jpeg)(?:\?[^"\'<>)\s]*)?)["\']',
            # URLs relativas sin comillas
            r'(/[^"\'<>)\s]+\.(jpg|jpeg)(?:\?[^"\'<>)\s]*)?)',
        ]
        base_url = ImageUrlScraper.BASE_URL
        for pattern in jpg_patterns:
            matches = re.finditer(pattern, html_content, re.IGNORECASE)
            for match in matches:
                url = match.group(1) if match.lastindex and match.lastindex >= 1 else match.group(0)
                if url:
                    # Normalizar la URL a absoluta
                    absolute_url = ImageUrlScraper._get_absolute_url_from_html(url)
                    if absolute_url and absolute_url not in seen_urls:
                        # Verificar que sea JPG/JPEG
                        url_lower = absolute_url.lower()
                        if '.jpg' in url_lower or '.jpeg' in url_lower:
                            seen_urls.add(absolute_url)
                            filename = _extract_filename_from_url(absolute_url)
                            if filename:
                                image_urls_map[filename] = absolute_url
        
        logger.debug(f'Encontradas {len(image_urls_map)} URLs absolutas scrapeadas del HTML')
        return image_urls_map
    
    @staticmethod
    def _extract_urls_from_json(obj, urls: Optional[set] = None) -> set:
        """Extrae URLs de imágenes de un objeto JSON recursivamente."""
        if urls is None:
            urls = set()
        
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, str):
                    # Verificar si es una URL de imagen
                    if any(ext in value.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']) or 'imgix' in value.lower():
                        urls.add(value)
                else:
                    ImageUrlScraper._extract_urls_from_json(value, urls)
        elif isinstance(obj, list):
            for item in obj:
                ImageUrlScraper._extract_urls_from_json(item, urls)
        
        return urls
    
    @staticmethod
    def _resolve_image_url(image_url: Optional[str], image_urls_map: Dict[str, str]) -> Optional[str]:
        """
        Resuelve una URL de imagen usando el mapeo extraído del HTML.
        
        Args:
            image_url: URL o ruta relativa de la imagen del JSON
            image_urls_map: Diccionario de URLs encontradas en el HTML
            
        Returns:
            URL completa de la imagen o la original si no se encuentra
        """
        if not image_url:
            return None
        
        # Si ya es una URL absoluta, retornarla
        if image_url.startswith('http://') or image_url.startswith('https://'):
            return image_url
        
        base_url = ImageUrlScraper.BASE_URL
        
        # Buscar en el mapeo usando diferentes estrategias
        # 1. Buscar la ruta relativa directamente
        if image_url in image_urls_map:
            logger.debug('URL encontrada en mapeo (ruta completa): %s -> %s', image_url, image_urls_map[image_url])
            return image_urls_map[image_url]
        
        # 2. Buscar por nombre de archivo
        filename = _extract_filename_from_url(image_url)
        if filename and filename in image_urls_map:
            logger.debug('URL encontrada en mapeo (nombre archivo): %s -> %s', filename, image_urls_map[filename])
            return image_urls_map[filename]
        
        # 3. Buscar coincidencias parciales (el nombre del archivo puede estar en cualquier ruta)
        if filename:
            for key, value in image_urls_map.items():
                if filename in key or key.endswith(filename):
                    logger.debug('URL encontrada en mapeo (coincidencia parcial): %s -> %s', image_url, value)
                    return value
        
        # 4. Si no se encuentra, construir URL estándar
        if image_url.startswith('/'):
            constructed_url = f'{base_url}{image_url}'
        else:
            constructed_url = f'{base_url}/{image_url}'
        
        logger.debug('URL construida (no encontrada en mapeo): %s -> %s', image_url, constructed_url)
        return constructed_url

    @staticmethod
    def _safe_amount(value: Optional[Dict[str, Any]]) -> Optional[float]:
        if not value:
            return None
        amount = value.get('amount')
        if isinstance(amount, (int, float)):
            return float(amount)
        try:
            return float(amount)
        except (TypeError, ValueError):
            return None
