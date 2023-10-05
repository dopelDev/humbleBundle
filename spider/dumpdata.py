from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import Session
from settings import get_settings
from models import Base, Bundle

settings = get_settings()

def get_session_factory(settings): 
    uri = f'postgresql+psycopg2://{settings.pguser}:{settings.pgpassword}@{settings.pghost}:{settings.pgport}/{settings.pgdatabase}'
    engine = create_engine(uri, echo = True)
    if not database_exists(uri):
        create_database(uri)
    Base.metadata.create_all(engine)
    session = Session(bind=engine)
    return session

def parse_sql(data, session):
    try:
        for _, row in data.iterrows():
            bundle_instance = Bundle(
                    machine_name = row['machine_name'],
                    high_res_tile_image = row['high_res_tile_image'],
                    disable_hero_tile = row['disable_hero_tile'],
                    marketing_blurb = row['marketing_blurb'],
                    hover_title = row['hover_title'],
                    product_url = row['product_url'],
                    tile_image = row['tile_image'],
                    category = row['category'],
                    hero_highlights = row['hero_highlights'],
                    hover_highlights = row['hover_highlights'],
                    author = row['author'],
                    supports_partners = row['supports_partners'],
                    detailed_marketing_blurb = row['detailed_marketing_blurb'],
                    tile_logo = row['tile_logo'],
                    tile_short_name = row['tile_short_name'],
                    start_date_datetime = row['start_date|datetime'],
                    end_date_datetime = row['end_date|datetime'],
                    tile_stamp = row['tile_stamp'],
                    bundles_sold_decimal = row['bundles_sold|decimal'],
                    tile_name = row['tile_name'],
                    short_marketing_blurb = row['short_marketing_blurb'],
                    _type = row['type'],
                    highlights = row['highlights'],
                    tile_logo_information_config_image_type = row['tile_logo_information.config.image_type'],
                    tile_logo_information_config_gcs = row['tile_logo_information.config.gcs'],
                    tile_logo_information_config_imgix_master_image_image_type = row['tile_logo_information.config.imgix.master_image.image_type'],
                    high_res_tile_image_information_config_image_type = row['high_res_tile_image_information.config.image_type'],
                    high_res_tile_image_information_config_gcs = row['high_res_tile_image_information.config.gcs'],
                    high_res_tile_image_information_config_imgix_master_image_image_type = row['high_res_tile_image_information.config.imgix.master_image.image_type'],
                    tile_image_information_config_image_type = row['tile_image_information.config.image_type'],
                    tile_image_information_config_gcs = row['tile_image_information.config.gcs'],
                    tile_image_information_config_imgix_master_image_image_type = row['tile_image_information.config.imgix.master_image.image_type']
                    )
            session.add(bundle_instance)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f'Error dump data: {e}')
    finally:
        session.close()

