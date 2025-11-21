export interface ScrapedImageURL {
  id: string;
  bundle_id: string;
  url: string;
  source?: string | null; // 'img_tag', 'style', 'data_attr', 'json', 'regex'
  attribute?: string | null; // 'src', 'data-src', 'background-image', etc.
  scraped_date: string;
}

