from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, JSON, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4

Base = declarative_base()

class Bundle(Base):
    """
    Modelo ORM para representar un bundle de Humble Bundle.
    
    Almacena toda la información de un bundle incluyendo metadatos,
    fechas, imágenes, precios y lista de libros.
    """
    __tablename__ = 'bundle'
    __table_args__ = ()

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    machine_name = Column(String, unique=True, index=True, nullable=False)
    high_res_tile_image = Column(String)
    disable_hero_tile = Column(Boolean)
    marketing_blurb = Column(String)
    hover_title = Column(String)
    product_url = Column(String)
    tile_image = Column(String)
    category = Column(String)
    hero_highlights = Column(String)
    hover_highlights = Column(String)
    author = Column(String)
    supports_partners = Column(Boolean)
    detailed_marketing_blurb = Column(String)
    tile_logo = Column(String)
    tile_short_name = Column(String)
    start_date_datetime = Column(DateTime, index=True)
    end_date_datetime = Column(DateTime, index=True)
    tile_stamp = Column(String)
    bundles_sold_decimal = Column(Float)
    tile_name = Column(String)
    short_marketing_blurb = Column(String)
    _type = Column(String)
    highlights = Column(String)
    tile_logo_information_config_image_type = Column(String)
    tile_logo_information_config_gcs = Column(String)
    tile_logo_information_config_imgix_master_image_image_type = Column(String)
    high_res_tile_image_information_config_image_type = Column(String)
    high_res_tile_image_information_config_gcs = Column(String)
    high_res_tile_image_information_config_imgix_master_image_image_type = Column(String)
    tile_image_information_config_image_type = Column(String)
    tile_image_information_config_gcs = Column(String)
    tile_image_information_config_imgix_master_image_image_type = Column(String)
    verification_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    duration_days = Column(Float)
    is_active = Column(Boolean, default=False, index=True)
    price_tiers = Column(JSON)
    book_list = Column(JSON)
    featured_image = Column(String)
    msrp_total = Column(Float)
    raw_html = Column(String)  # HTML raw del bundle para tests


class LandingPageRawData(Base):
    """
    Modelo ORM para almacenar el JSON raw de landingPage-json-data.
    
    Almacena el JSON completo obtenido del script landingPage-json-data
    en cada ejecución del ETL, junto con metadata como fecha de scraping,
    URL fuente, hash del JSON y versión.
    """
    __tablename__ = 'landing_page_raw_data'
    __table_args__ = ()

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    json_data = Column(JSONB, nullable=False)
    scraped_date = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    source_url = Column(String, nullable=False)
    json_hash = Column(String, nullable=True, index=True)
    json_version = Column(String, nullable=True)
