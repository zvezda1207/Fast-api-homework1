from fastapi import FastAPI, Query
from schema import (CreateAdvRequest, UpdateAdvRequest, CreateAdvResponse, UpdateAdvResponse,
                     GetAdvResponse, SearchAdvResponse, DeleteAdvResponse)
from lifespan import lifespan
from sqlalchemy import select, DateTime

from dependency import SessionDependency
from constants import SUCCESS_RESPONSE
import models
import crud
from datetime import datetime


app = FastAPI(title='Adv API', description='Adv app', price='Adv price', author='Adv author', created_at='Adv date', lifespan=lifespan)


@app.post('/api/v1/adv', tags=['adv'], response_model=CreateAdvResponse)
async def create_adv(adv: CreateAdvRequest, session: SessionDependency):
    adv_dict = adv.model_dump(exclude_unset=True)
    adv_orm_obj = models.Adv(**adv_dict)
    await crud.add_item(session, adv_orm_obj)
    return adv_orm_obj.id_dict
    
@app.patch('/api/v1/adv/{adv_id}', response_model=UpdateAdvResponse)
async def update_adv(adv_id: int, adv_data: UpdateAdvRequest, session: SessionDependency):
    adv_dict = adv_data.model_dump(exclude_unset=True)
    adv_orm_obj = await crud.get_item_by_id(session, models.Adv, adv_id)
    for field, value in adv_dict.items():
        setattr(adv_orm_obj, field, value)
    await crud.update_item(session, adv_orm_obj)
    return SUCCESS_RESPONSE

@app.get('/api/v1/adv/{adv_id}', tags=['adv'], response_model=GetAdvResponse)
async def get_adv(adv_id: int, session: SessionDependency):
    adv_orm_obj = await crud.get_item_by_id(session, models.Adv, adv_id)
    return adv_orm_obj.dict

@app.get('/api/v1/adv', response_model=SearchAdvResponse)
async def search_adv(
    session: SessionDependency, 
    title: str | None = None,
    description: str | None = None,
    price_from: float | None = None,
    price_to: float | None = None,
    author: str | None = None,
    created_after: datetime | None = Query(None),
    created_before: datetime | None = Query(None)
    ):
    filters = []
    if title:
        filters.append(models.Adv.title.ilike(f'%{title}%'))
    if description:
        filters.append(models.Adv.description.ilike(f'%{description}%'))
    if price_from is not None:
        filters.append(models.Adv.price >= price_from)
    if price_to is not None:
        filters.append(models.Adv.price <= price_to)
    if author:
        filters.append(models.Adv.author.ilike(f'%{author}%'))
    if created_after:
        filters.append(models.Adv.created_at >= created_after)
    if created_before:
        filters.append(models.Adv.created_at <= created_before)

    query = select(models.Adv)
    if filters:
        query = query.where(*filters)

    result = await session.scalars(query)
    advs = result.all()
    return {'results': [adv.dict for adv in advs]}

@app.delete('/api/v1/adv/{adv_id}', response_model=DeleteAdvResponse)
async def delete_adv(adv_id: int, session: SessionDependency):
    adv_orm_obj = await crud.get_item_by_id(session, models.Adv, adv_id)
    await crud.delete_item(session, adv_orm_obj)
    return SUCCESS_RESPONSE







