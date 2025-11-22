# Humble Bundle Image URL Patterns

## Summary

This document describes the image URL patterns used by Humble Bundle for their bundles and books.

## Identified Patterns

### 1. Book Images (Book List)

**Pattern:**
```
/images/popups/{machine_name}_slideout.jpg
```

**Complete URL:**
```
https://www.humblebundle.com/images/popups/{machine_name}_slideout.jpg
```

**Description:**
- All book images in a bundle's item list follow this pattern
- The `{machine_name}` is the unique identifier of the book from the bundle JSON
- The extension is always `.jpg`
- The suffix is always `_slideout.jpg`

**Examples:**
- `spaceghost2024_issue12` → `https://www.humblebundle.com/images/popups/spaceghost2024_issue12_slideout.jpg`
- `herculoids_issue1` → `https://www.humblebundle.com/images/popups/herculoids_issue1_slideout.jpg`
- `thundercats_apex` → `https://www.humblebundle.com/images/popups/thundercats_apex_slideout.jpg`

**Extraction:**
URLs are extracted from bundle HTML using BeautifulSoup, searching in:
- `<img>` tags with attributes `src`, `data-src`, `data-lazy-src`, `data-original`
- `style` attributes with `background-image: url(...)`
- `data-image` attributes
- Regex in HTML content as fallback

### 2. Featured Image (Bundle Logo)

**Pattern:**
Depends on image type:

**Option A - Imgix CDN:**
```
https://hb.imgix.net/{hash}.{ext}?auto=compress,format&h={height}&w={width}&s={signature}
```

**Option B - Direct URL:**
```
{direct_url_from_json}
```

**Description:**
- The bundle's featured image comes from the `logo` field in `basic_data` of the JSON
- It may use Humble Bundle's imgix CDN service
- Imgix parameters include dimensions and automatic compression

**Example:**
```
https://hb.imgix.net/a3f1903aee43441e9bbc0ad6cf207698dac696d6.png?auto=compress,format&h=340&w=1200&s=71909e2bb3f147ab7d76471b89901996
```

**Extraction:**
The URL comes directly from the bundle JSON in the `bundleData.basic_data.logo` field.

## Implementation

### Backend (Spider)

Extraction code is located in:
- `spider/scrapers/image_scraper.py`:
  - `_extract_jpg_urls_from_html()`: Extracts URLs from HTML using BeautifulSoup
  - `_resolve_image_url()`: Resolves URLs using mapping extracted from HTML

### Frontend

The frontend should use URLs directly from the bundle JSON, without additional construction.

**Data structure:**
```typescript
interface BookItem {
  machine_name: string;
  title: string;
  image: string; // Complete image URL
  // ... other fields
}

interface Bundle {
  featured_image: string; // Complete featured image URL
  book_list: BookItem[];
  // ... other fields
}
```

## Technical Notes

1. **Absolute URLs**: All returned URLs are absolute (complete), no additional construction needed.

2. **CORS**: Humble Bundle images are served with appropriate CORS headers, allowing direct loading from any domain.

3. **Cache**: Images can be cached by the browser normally.

4. **Fallback**: If a URL is not found in HTML, the system constructs the standard URL using the known pattern.

5. **Validation**: Code validates that URLs are valid before storing them in the database.

## References

- Humble Bundle base URL: `https://www.humblebundle.com`
- Image CDN: `https://hb.imgix.net`
- Image directory structure: `/images/popups/`
