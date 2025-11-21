from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator
from pydantic.config import ConfigDict


class BundleRecord(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        extra='ignore',
        protected_namespaces=(),
    )

    machine_name: str = Field(max_length=255)
    high_res_tile_image: Optional[str] = Field(default=None, max_length=2048)
    disable_hero_tile: Optional[bool] = None
    marketing_blurb: Optional[str] = Field(default=None, max_length=1024)
    hover_title: Optional[str] = Field(default=None, max_length=255)
    product_url: Optional[HttpUrl] = None
    tile_image: Optional[str] = Field(default=None, max_length=2048)
    category: Optional[str] = Field(default=None, max_length=128)
    hero_highlights: Optional[str] = None
    hover_highlights: Optional[str] = None
    author: Optional[str] = Field(default=None, max_length=255)
    supports_partners: Optional[bool] = None
    detailed_marketing_blurb: Optional[str] = Field(default=None, max_length=2048)
    tile_logo: Optional[str] = Field(default=None, max_length=2048)
    tile_short_name: Optional[str] = Field(default=None, max_length=255)
    start_date_datetime: datetime = Field(alias='start_date|datetime')
    end_date_datetime: datetime = Field(alias='end_date|datetime')
    tile_stamp: Optional[str] = Field(default=None, max_length=64)
    bundles_sold_decimal: Optional[float] = Field(default=None, alias='bundles_sold|decimal')
    tile_name: Optional[str] = Field(default=None, max_length=255)
    short_marketing_blurb: Optional[str] = Field(default=None, max_length=512)
    type_value: Optional[str] = Field(default=None, alias='type')
    highlights: Optional[str] = None
    tile_logo_information_config_image_type: Optional[str] = Field(
        default=None,
        alias='tile_logo_information.config.image_type',
    )
    tile_logo_information_config_gcs: Optional[str] = Field(
        default=None,
        alias='tile_logo_information.config.gcs',
    )
    tile_logo_information_config_imgix_master_image_image_type: Optional[str] = Field(
        default=None,
        alias='tile_logo_information.config.imgix.master_image.image_type',
    )
    high_res_tile_image_information_config_image_type: Optional[str] = Field(
        default=None,
        alias='high_res_tile_image_information.config.image_type',
    )
    high_res_tile_image_information_config_gcs: Optional[str] = Field(
        default=None,
        alias='high_res_tile_image_information.config.gcs',
    )
    high_res_tile_image_information_config_imgix_master_image_image_type: Optional[str] = Field(
        default=None,
        alias='high_res_tile_image_information.config.imgix.master_image.image_type',
    )
    tile_image_information_config_image_type: Optional[str] = Field(
        default=None,
        alias='tile_image_information.config.image_type',
    )
    tile_image_information_config_gcs: Optional[str] = Field(
        default=None,
        alias='tile_image_information.config.gcs',
    )
    tile_image_information_config_imgix_master_image_image_type: Optional[str] = Field(
        default=None,
        alias='tile_image_information.config.imgix.master_image.image_type',
    )
    verification_date: datetime = Field(default_factory=datetime.utcnow)
    duration_days: Optional[float] = None
    is_active: bool = False
    price_tiers: Optional[List[Dict[str, object]]] = None
    book_list: Optional[List[Dict[str, object]]] = None
    featured_image: Optional[str] = Field(default=None, max_length=2048)
    msrp_total: Optional[float] = None
    raw_html: Optional[str] = Field(default=None, description='HTML raw del bundle para tests')

    @field_validator('hero_highlights', 'hover_highlights', 'highlights', mode='before')
    @classmethod
    def ensure_string(cls, value):
        if value is None:
            return value
        return str(value)

    @field_validator('bundles_sold_decimal', 'duration_days', mode='before')
    @classmethod
    def ensure_non_negative(cls, value):
        if value is None:
            return None
        try:
            value = float(value)
        except (TypeError, ValueError):
            return None
        return value if value >= 0 else None

    def to_orm_payload(self) -> dict:
        payload = self.model_dump()
        payload['_type'] = payload.pop('type_value')
        if payload.get('product_url'):
            payload['product_url'] = str(payload['product_url'])
        return payload

