from sqlalchemy import Column, String, Boolean, DateTime, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4

Base = declarative_base()

class Bundle(Base):
    __tablename__ = 'bundle'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    hash_id = Column(String(length=1024), unique=True)
    machine_name = Column(String(length=1024))
    high_res_tile_image = Column(String(length=1024))
    disable_hero_tile = Column(Boolean)
    marketing_blurb = Column(String(length=1024))
    hover_title = Column(String(length=1024))
    product_url = Column(String(length=1024))
    tile_image = Column(String(length=1024))
    category = Column(String(length=1024))
    hero_highlights = Column(String(length=1024))
    hover_highlights = Column(String(length=1024))
    author = Column(String(length=1024))
    supports_partners = Column(Boolean)
    detailed_marketing_blurb = Column(String(length=1024))
    tile_logo = Column(String(length=1024))
    tile_short_name = Column(String(length=1024))
    start_date_datetime = Column(DateTime)
    end_date_datetime = Column(DateTime)
    tile_stamp = Column(String(length=1024))
    bundles_sold_decimal = Column(Float)
    tile_name = Column(String(length=1024))
    short_marketing_blurb = Column(String(length=1024))
    _type = Column(String(length=1024))
    highlights = Column(String(length=1024))
    tile_logo_information_config_image_type = Column(String(length=1024))
    tile_logo_information_config_gcs = Column(String(length=1024))
    tile_logo_information_config_imgix_master_image_image_type = Column(String(length=1024))
    high_res_tile_image_information_config_image_type = Column(String(length=1024))
    high_res_tile_image_information_config_gcs = Column(String(length=1024))
    high_res_tile_image_information_config_imgix_master_image_image_type = Column(String(length=1024))
    tile_image_information_config_image_type = Column(String(length=1024))
    tile_image_information_config_gcs = Column(String(length=1024))
    tile_image_information_config_imgix_master_image_image_type = Column(String(length=1024))

