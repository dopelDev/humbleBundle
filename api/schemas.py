from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class BundleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
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
    tile_logo: Optional[str] = None
    msrp_total: Optional[float] = None
    raw_html: Optional[str] = None
    verification_date: datetime


class ETLRunResponse(BaseModel):
    bundles_processed: int
    cleanup_ran: bool


class LandingPageRawDataResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    json_data: Dict[str, Any]
    scraped_date: datetime
    source_url: str
    json_hash: Optional[str] = None
    json_version: Optional[str] = None



