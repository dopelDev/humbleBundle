from uuid import UUID
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import nulls_last, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import Session

import logging

from spider.database.session import get_session_factory as build_session_factory
from spider.database.persistence import persist_bundles, remove_outdated_bundles, persist_landing_page_raw_data
from spider.core.spider import HumbleSpider
from spider.core.errors import HumbleSpiderError
from spider.database.models import Bundle, LandingPageRawData
from spider.config.settings import get_settings

logger = logging.getLogger(__name__)

from api.schemas import BundleResponse, ETLRunResponse, LandingPageRawDataResponse

settings = get_settings()
SessionFactory = None
AsyncSessionFactory = None

def get_async_engine():
    """Creates the async engine for FastAPI."""
    uri = f'postgresql+asyncpg://{settings.pguser}:{settings.pgpassword}@{settings.pghost}:{settings.pgport}/{settings.pgdatabase}'
    return create_async_engine(uri, echo=settings.sql_echo, future=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan to initialize async resources."""
    global AsyncSessionFactory
    async_engine = get_async_engine()
    
    # Create tables if they don't exist using the async engine
    from spider.database.models import Base
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)
    
    # Ensure columns exist (works better with sync)
    from spider.database.persistence import ensure_columns, ensure_landing_page_raw_data_table
    from sqlalchemy import create_engine
    sync_engine = create_engine(
        f'postgresql+psycopg://{settings.pguser}:{settings.pgpassword}@{settings.pghost}:{settings.pgport}/{settings.pgdatabase}',
        echo=settings.sql_echo,
        future=True
    )
    try:
        ensure_columns(sync_engine)
        ensure_landing_page_raw_data_table(sync_engine)
    finally:
        sync_engine.dispose()
    
    AsyncSessionFactory = async_sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    yield
    await async_engine.dispose()

app = FastAPI(
    title='Humble Bundle ETL API',
    version='1.0.0',
    description='API to trigger the ETL and query stored bundles.',
    lifespan=lifespan
)

allowed_origins = [
    'http://localhost:3002',
    'http://127.0.0.1:3002',
    'http://frontend:3002',
    'http://localhost:3003',
    'http://127.0.0.1:3003',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Montar directorio de imágenes estáticas
import os
from pathlib import Path

images_dir = Path("/app/images")
# Crear directorios si no existen
images_dir.mkdir(parents=True, exist_ok=True)
(images_dir / "bundles").mkdir(parents=True, exist_ok=True)
(images_dir / "books").mkdir(parents=True, exist_ok=True)

app.mount("/images", StaticFiles(directory=str(images_dir)), name="images")


def get_db():
    global SessionFactory
    if SessionFactory is None:
        SessionFactory = build_session_factory(settings)
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()


async def get_async_db():
    """Async session for async endpoints."""
    global AsyncSessionFactory
    if AsyncSessionFactory is None:
        async_engine = get_async_engine()
        AsyncSessionFactory = async_sessionmaker(
            async_engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
    async with AsyncSessionFactory() as session:
        try:
            yield session
        finally:
            await session.close()


@app.get('/health', tags=['health'])
async def healthcheck():
    return {'status': 'ok', 'database': settings.pgdatabase}


@app.get('/bundles/featured', response_model=BundleResponse, tags=['bundles'])
async def get_featured_bundle(db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(
        select(Bundle).order_by(
            nulls_last(Bundle.msrp_total.desc()),
            nulls_last(Bundle.bundles_sold_decimal.desc()),
        ).limit(1)
    )
    bundle = result.scalar_one_or_none()
    if not bundle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No bundles stored')
    return bundle


@app.get('/bundles', response_model=list[BundleResponse], tags=['bundles'])
async def list_bundles(db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(
        select(Bundle).order_by(Bundle.end_date_datetime.desc())
    )
    bundles = result.scalars().all()
    return bundles


@app.get('/bundles/{bundle_id}', response_model=BundleResponse, tags=['bundles'])
async def get_bundle(bundle_id: UUID, db: AsyncSession = Depends(get_async_db)):
    """Gets a bundle by its UUID."""
    result = await db.execute(
        select(Bundle).filter(Bundle.id == bundle_id)
    )
    bundle = result.scalar_one_or_none()
    if not bundle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Bundle not found')
    return bundle


@app.get('/bundles/by-machine-name/{machine_name}', response_model=BundleResponse, tags=['bundles'])
async def get_bundle_by_machine_name(machine_name: str, db: AsyncSession = Depends(get_async_db)):
    """Gets a bundle by its machine_name (backward compatibility)."""
    result = await db.execute(
        select(Bundle).filter(Bundle.machine_name == machine_name)
    )
    bundle = result.scalar_one_or_none()
    if not bundle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Bundle not found')
    return bundle


@app.post('/etl/run', response_model=ETLRunResponse, tags=['etl'])
def trigger_etl(db: Session = Depends(get_db)):
    """Executes the complete ETL: downloads bundles, downloads images and saves to the database."""
    spider = HumbleSpider()
    try:
        records = spider.fetch_bundles()
    except HumbleSpiderError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc

    remove_outdated_bundles(db)
    persist_bundles(records, db)
    
    # Save landing page raw data
    raw_data_record = spider.get_raw_data_record()
    if raw_data_record:
        persist_landing_page_raw_data(raw_data_record, db)
    
    return ETLRunResponse(
        bundles_processed=len(records),
        cleanup_ran=True,
        images_downloaded=0,
        bundle_images_downloaded=0,
        book_images_downloaded=0,
        images_info=[]
    )


@app.get('/landing-page-raw-data', response_model=list[LandingPageRawDataResponse], tags=['raw-data'])
async def list_landing_page_raw_data(db: AsyncSession = Depends(get_async_db)):
    """Lists all raw data records ordered by descending date."""
    result = await db.execute(
        select(LandingPageRawData).order_by(LandingPageRawData.scraped_date.desc())
    )
    raw_data_list = result.scalars().all()
    return raw_data_list


@app.get('/landing-page-raw-data/latest', response_model=LandingPageRawDataResponse, tags=['raw-data'])
async def get_latest_landing_page_raw_data(db: AsyncSession = Depends(get_async_db)):
    """Gets the most recent raw data record."""
    result = await db.execute(
        select(LandingPageRawData).order_by(LandingPageRawData.scraped_date.desc()).limit(1)
    )
    raw_data = result.scalar_one_or_none()
    if not raw_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No raw data stored')
    return raw_data


@app.get('/landing-page-raw-data/{raw_data_id}', response_model=LandingPageRawDataResponse, tags=['raw-data'])
async def get_landing_page_raw_data(raw_data_id: UUID, db: AsyncSession = Depends(get_async_db)):
    """Gets a specific raw data record by its ID."""
    result = await db.execute(
        select(LandingPageRawData).filter(LandingPageRawData.id == raw_data_id)
    )
    raw_data = result.scalar_one_or_none()
    if not raw_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Raw data not found')
    return raw_data


