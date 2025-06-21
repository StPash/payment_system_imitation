from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, declared_attr
from src.app.config import settings


engine = create_async_engine(settings.DATABASE_URL, echo=True)
new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with new_session() as session:
        yield session


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

