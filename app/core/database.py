from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import DATABASE_URL


# Tạo engine kết nối với cơ sở dữ liệu
engine = create_async_engine(DATABASE_URL) # thêm echo = True để bật logging SQL

# Tạo session factory
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Base cho các model
Base = declarative_base()

