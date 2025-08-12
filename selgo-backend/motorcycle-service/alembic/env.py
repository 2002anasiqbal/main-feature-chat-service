from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import your models - try multiple import paths
try:
    from src.models.models import Base
    print("✅ Successfully imported Base from src.models.models")
except ImportError as e:
    print(f"❌ Failed to import from src.models.models: {e}")
    try:
        # Alternative import path
        from models.models import Base
        print("✅ Successfully imported Base from models.models")
    except ImportError as e2:
        print(f"❌ Failed to import from models.models: {e2}")
        # Create empty Base as fallback
        from sqlalchemy.ext.declarative import declarative_base
        Base = declarative_base()
        print("⚠️ Using empty Base - no tables will be detected")

config = context.config

def get_database_url():
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "12345")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "selgo_motorcycle")
    
    return f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

config.set_main_option('sqlalchemy.url', get_database_url())

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def include_object(object, name, type_, reflected, compare_to):
    """Exclude PostGIS tables"""
    if type_ == "table" and name in [
        'spatial_ref_sys',
        'geography_columns', 
        'geometry_columns',
        'raster_columns',
        'raster_overviews'
    ]:
        return False
    return True

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            include_object=include_object,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()