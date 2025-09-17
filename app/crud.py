from fastapi import HTTPException
from models import ORM_OBJ, ORM_CLS, Adv
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

async def add_item(session: AsyncSession, item: ORM_OBJ):
    session.add(item)
    try:
        await session.commit()
    except IntegrityError as err:
        print(f"IntegrityError: {err}")
        raise HTTPException(409, 'Item already exist')
    
async def update_item(session: AsyncSession, item: ORM_OBJ):
    try:
        await session.commit()
    except IntegrityError as err:
        raise HTTPException(409, 'Update conflict')

async def get_item_by_id(session: AsyncSession, orm_cls: ORM_CLS, item_id: int) -> ORM_OBJ:
    orm_obj = await session.get(orm_cls, item_id)
    if orm_obj is None:
        raise HTTPException(404, f'Item not found')
    return orm_obj

async def delete_item(session: AsyncSession, item: ORM_OBJ):
    await session.delete(item)
    await session.commit()