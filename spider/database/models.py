from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, JSON, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from uuid import uuid4

Base = declarative_base()

class Bundle(Base):
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
    
    # Relación con ImageURL
    image_urls = relationship("ImageURL", back_populates="bundle", cascade="all, delete-orphan")
    
    # Relación con ScrapedImageURL
    scraped_image_urls = relationship("ScrapedImageURL", back_populates="bundle", cascade="all, delete-orphan")


class ScrapedImageURL(Base):
    """
    Entidad para almacenar TODAS las URLs de imágenes scrapeadas del HTML de cada bundle.
    Estas son las URLs absolutas extraídas con BeautifulSoup del raw_html (imgix, cdn, etc.).
    Se guardan durante el ETL para tener una muestra real de URLs del HTML.
    """
    __tablename__ = 'scraped_image_url'
    __table_args__ = ()

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    bundle_id = Column(UUID(as_uuid=True), ForeignKey('bundle.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # URL absoluta scrapeada del HTML (imgix, cdn, etc.)
    url = Column(String, nullable=False)
    
    # Origen de donde se encontró: 'img_tag', 'style', 'data_attr', 'json', 'regex'
    source = Column(String, nullable=True)
    
    # Atributo específico si aplica (ej: 'src', 'data-src', 'background-image')
    attribute = Column(String, nullable=True)
    
    # Fecha de scraping (cuando se ejecutó el ETL)
    scraped_date = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relación con Bundle
    bundle = relationship("Bundle", back_populates="scraped_image_urls")


class ImageURL(Base):
    """
    Entidad relacionada para almacenar las URLs reales de imágenes encontradas en el HTML.
    Relacionada con Bundle y almacena el real_path encontrado mediante ingeniería inversa.
    """
    __tablename__ = 'image_url'
    __table_args__ = ()

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    bundle_id = Column(UUID(as_uuid=True), ForeignKey('bundle.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Tipo de imagen: 'featured_image' o 'book_image'
    image_type = Column(String, nullable=False, index=True)
    
    # Machine name del libro (solo para book_image)
    book_machine_name = Column(String, nullable=True, index=True)
    
    # URL original almacenada en la BD (del campo image)
    original_url = Column(String, nullable=False)
    
    # URL real encontrada en el HTML (real_path)
    real_path = Column(String, nullable=True)
    
    # Tipo de match encontrado: 'exact', 'filename', 'path_segment', 'partial', o None si no hubo match
    match_type = Column(String, nullable=True)
    
    # Fecha de verificación
    verification_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relación con Bundle
    bundle = relationship("Bundle", back_populates="image_urls")

