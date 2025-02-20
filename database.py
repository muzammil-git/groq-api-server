from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# [prod] : Will move to .env
HOST = 'localhost'
PORT = 5432
USERNAME = 'postgres'
PASSWORD = 'postgres'
DATABASE = 'test_db'

# postgresql://USER:PASSWORD@INTERNAL_HOST:PORT/DATABASE
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,  # Ensure the session is asynchronous
    expire_on_commit=False,  # Prevent SQLAlchemy from expiring objects after commit
)

Base = declarative_base()


async def get_db() -> AsyncSession: # type: ignore
    async with SessionLocal() as db:
        try:
            yield db
        except Exception as e:
            print(f"Error; database.py : {e}")
        finally:
            await db.close()