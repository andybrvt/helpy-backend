from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base


# Database URL: Replace with your PostgreSQL credentials
# postgresql+asyncpg://<username>:<password>@<host>:<port>/<database_name>
DATABASE_URL = "postgresql+asyncpg://andyle:password@localhost:5432/helpydb"

# Create the engine (asynchronous)
engine = create_async_engine(DATABASE_URL, echo=True)

# Session factory (asynchronous)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Base class for models
Base = declarative_base()


# Dependency for FastAPI routes to get the database session
async def get_db():
    async with SessionLocal() as session:
        yield session