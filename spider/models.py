from sqlalchemy import Column, String, Boolean, DateTime, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4

Base = declarative_base()

class Bundle(Base):
    __tablename__ = 'bundle'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    machine_name = Column(String)
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
    start_date_datetime = Column(DateTime)
    end_date_datetime = Column(DateTime)
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

