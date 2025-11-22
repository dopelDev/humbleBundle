export interface LandingPageRawData {
  id: string;
  json_data: Record<string, unknown>;
  scraped_date: string;
  source_url: string;
  json_hash: string | null;
  json_version: string | null;
}

