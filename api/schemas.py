from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BundleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    machine_name: str
    tile_name: Optional[str] = None
    tile_short_name: Optional[str] = None
    tile_stamp: Optional[str] = None
    category: Optional[str] = None
    product_url: Optional[str] = None
    start_date_datetime: Optional[datetime] = None
    end_date_datetime: Optional[datetime] = None
    duration_days: Optional[float] = None
    is_active: Optional[bool] = None
    price_tiers: Optional[List[Dict[str, Any]]] = None
    book_list: Optional[List[Dict[str, Any]]] = None
    featured_image: Optional[str] = None
    msrp_total: Optional[float] = None
    raw_html: Optional[str] = None
    verification_date: datetime


class ETLRunResponse(BaseModel):
    bundles_processed: int
    cleanup_ran: bool
    images_downloaded: int = 0
    bundle_images_downloaded: int = 0
    book_images_downloaded: int = 0
    images_info: list[dict[str, str]] = []


class LandingPageRawDataResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    json_data: Dict[str, Any]
    scraped_date: datetime
    source_url: str
    json_hash: Optional[str] = None
    json_version: Optional[str] = None


