# Initial Humble Bundle Data Profiling

## Source
- Endpoint: `https://www.humblebundle.com/books`
- Method: downloads via `HumbleSpider` (`requests + BeautifulSoup`).
- Sampling date: `2025-11-20T02:52:44-05:00`

## Dataset Summary
- Total bundles in sample: **14**
- Columns after `pandas.json_normalize`: **32**
- Critical columns always present (no nulls detected):
  - `machine_name`, `tile_name`, `tile_short_name`, `tile_stamp`, `category`
  - `start_date|datetime`, `end_date|datetime`, `bundles_sold|decimal`
  - `*_information.config.*` blocks (images and logos)
- Columns with optional/missing values: `marketing_blurb`, `hover_title`, `supports_partners`, `hero_highlights`, `hover_highlights`, `author`, `tile_logo`, etc.
- Bundle-enriched data (from `webpack-bundle-page-data` script):
  - `price_tiers`: list of tiers with header, price and associated machine_names.
  - `book_list`: detail per book/comic (name, MSRP, image, tiers it belongs to).
  - `featured_image` (bundle logo) and `msrp_total` (officially communicated sum).

## Relevant Findings
- **Date fields** are already converted to `datetime64[ns, UTC]` but require `tz_localize` when exposing in API for consistency.
- **JSON lists** (`hero_highlights`, `hover_highlights`, `highlights`) must always be serialized to ordered string so Pydantic doesn't fail (already normalized, but needs documentation).
- `bundles_sold|decimal` arrives as decimal number represented in text; current conversion to `float64` works but must handle `NaN` when metric is missing.
- `verification_date` doesn't exist in source; it's generated internally (scraping timestamp) and must remain mandatory for auditing.
- `product_url` is relative; absolute URL must be constructed if external consumption is required.

## Suggested Next Actions
1. Define catalog of columns and expected types (include maximum `String` lengths in SQLAlchemy model).
2. Establish policies for nulls/empty values (e.g. `None` vs `''`) to avoid writing empty strings to database.
3. Record metrics for each run (bundles processed, discarded, missing fields) to monitor source changes.
4. Create unit tests that validate against payload fixtures (at least two snapshots with different structures).
5. Version the detail JSON structure to detect changes in `tier_pricing_data` or `tier_item_data`.
