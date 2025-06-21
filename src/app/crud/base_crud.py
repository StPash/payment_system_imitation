from typing import Type, TypeVar, List

from sqlalchemy import select, inspect
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.database import Base
from src.app.models.user import User

ModelType = TypeVar("ModelType", bound=Base)


class CRUDBase:
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> ModelType | None:
        """Получение сущности по id"""
        return await db.get(self.model, id)

    async def get_by(self, db: AsyncSession, **kwargs) -> ModelType | None:
        """Получение сущности по атрибуту / атрибутам"""
        return (await db.scalars(select(self.model).filter_by(**kwargs))).first()

    async def get_all(self, db: AsyncSession) -> List[ModelType] | None:
        """Получение всех сущностей"""
        return list((await db.scalars(select(self.model))).unique().all())

    async def create(
            self, db: AsyncSession, data: dict
    ) -> ModelType:
        db_obj = self.model(**data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
            self, db: AsyncSession, db_obj: ModelType, data: dict
    ) -> ModelType:
        info = inspect(self.model)
        for field in info.columns.keys():
            if field in data:
                setattr(db_obj, field, data[field])
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove_obj(self, db: AsyncSession, obj: ModelType) -> ModelType:
        await db.delete(obj)
        await db.commit()
        return obj
