export interface PriceTier {
  identifier: string;
  header?: string;
  is_initial?: boolean;
  price?: {
    currency: string;
    amount: number;
  };
  items?: string[];
}

export interface BookItem {
  machine_name: string;
  title?: string;
  msrp?: number | null;
  preview?: Record<string, unknown> | null;
  image?: string | null;
  content_type?: string | null;
  tiers?: string[];
}

export interface Bundle {
  id: string;
  machine_name: string;
  tile_name?: string;
  tile_short_name?: string;
  category?: string;
  tile_stamp?: string;
  product_url?: string;
  duration_days?: number | null;
  is_active?: boolean;
  price_tiers?: PriceTier[];
  book_list?: BookItem[];
  featured_image?: string | null;
  msrp_total?: number | null;
  verification_date?: string;
  start_date_datetime?: string;
  end_date_datetime?: string;
}

