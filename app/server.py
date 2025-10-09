from fastapi import FastAPI, Query, HTTPException
from .schema import (CreateAdvRequest, UpdateAdvRequest, CreateAdvResponse, UpdateAdvResponse,
                     GetAdvResponse, SearchAdvResponse, DeleteAdvResponse, LoginRequest, LoginResponse,
                     CreateUserRequest, CreateUserResponse, GetUserResponse, UpdateUserResponse, 
                     UpdateUserRequest, DeleteUserResponse)
from .lifespan import lifespan
from sqlalchemy import select

from .dependency import SessionDependency, TokenDependency, OptionalTokenDependency
from .constants import SUCCESS_RESPONSE
from . import models
from . import crud
from datetime import datetime
from .auth import hash_password, check_password


app = FastAPI(title='Adv API', description='API for managing advertisements', lifespan=lifespan)

@app.get('/test')
async def test():
    return {'message': 'Test endpoint works'}

@app.post('/api/v1/adv', tags=['adv'], response_model=CreateAdvResponse)
async def create_adv(adv: CreateAdvRequest, session: SessionDependency, token: TokenDependency):
    try:
        print(f"Starting create_adv, token: {token}")
        print(f"Token user_id: {token.user_id}")
        
        adv_dict = adv.model_dump(exclude_unset=True)
        print(f"Adv dict: {adv_dict}")
        
        adv_orm_obj = models.Adv(**adv_dict, user_id=token.user_id)
        print(f"Created Adv object: {adv_orm_obj}")
        
        await crud.add_item(session, adv_orm_obj)
        print("Successfully added item")
        
        return adv_orm_obj.id_dict
    except Exception as e:
        print(f"Ошибка при создании объявления: {e}")
        import traceback
        traceback.print_exc()
        raise
    
@app.patch('/api/v1/adv/{adv_id}', response_model=UpdateAdvResponse)
async def update_adv(adv_id: int, adv_data: UpdateAdvRequest, session: SessionDependency, token: TokenDependency):
    adv_orm_obj = await crud.get_item_by_id(session, models.Adv, adv_id)
     # Проверяем права: только admin или автор объявления    
    if token.user.role != 'admin' and adv_orm_obj.user_id != token.user_id:
        raise HTTPException(403, 'Insufficient privileges')
    
    adv_dict = adv_data.model_dump(exclude_unset=True)
    for field, value in adv_dict.items():
        setattr(adv_orm_obj, field, value)
    await crud.update_item(session, adv_orm_obj)
    return SUCCESS_RESPONSE

@app.get('/api/v1/adv/{adv_id}', tags=['adv'], response_model=GetAdvResponse)
async def get_adv(adv_id: int, session: SessionDependency, token: OptionalTokenDependency = None):
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

    result = await session.execute(query)
    advs = result.scalars().all()
    return {'results': [adv.dict for adv in advs]}

@app.delete('/api/v1/adv/{adv_id}', response_model=DeleteAdvResponse)
async def delete_adv(adv_id: int, session: SessionDependency, token: TokenDependency):
    adv_orm_obj = await crud.get_item_by_id(session, models.Adv, adv_id)    
    # Проверяем права: только admin или автор объявления
    if token.user.role != 'admin' and adv_orm_obj.user_id != token.user_id:
        raise HTTPException(403, 'Insufficient privileges')    
    await crud.delete_item(session, adv_orm_obj)
    return SUCCESS_RESPONSE

@app.post('/api/v1/user', tags=['user'], response_model=CreateUserResponse)
async def create_user(user_data: CreateUserRequest, session: SessionDependency):
    user_dict = user_data.model_dump(exclude_unset=True)
    user_dict['password'] = hash_password(user_dict['password'])
    user_orm_obj = models.User(**user_dict)
    await crud.add_item(session, user_orm_obj)
    return user_orm_obj.dict

@app.get('/api/v1/user/{user_id}', tags=['user'], response_model=GetUserResponse)
async def get_user(user_id: int, session: SessionDependency, token: OptionalTokenDependency = None):
    user_orm_obj = await crud.get_item_by_id(session, models.User, user_id)    
    return user_orm_obj.dict


@app.patch('/api/v1/user/{user_id}', response_model=UpdateUserResponse)
async def update_user(user_id: int, user_data: UpdateUserRequest, session: SessionDependency, token: TokenDependency):
    user_orm_obj = await crud.get_item_by_id(session, models.User, user_id)    
    # Проверяем права: только admin или сам пользователь
    if token.user.role != 'admin' and user_orm_obj.id != token.user_id:
        raise HTTPException(403, 'Insufficient privileges')    
    user_dict = user_data.model_dump(exclude_unset=True)    
    # Если обновляется пароль, хешируем его
    if 'password' in user_dict:
        user_dict['password'] = hash_password(user_dict['password'])
    
    for field, value in user_dict.items():
        setattr(user_orm_obj, field, value)
    
    await crud.update_item(session, user_orm_obj)
    return SUCCESS_RESPONSE

@app.delete('/api/v1/user/{user_id}', response_model=DeleteUserResponse)
async def delete_user(user_id: int, session: SessionDependency, token: TokenDependency):
    user_orm_obj = await crud.get_item_by_id(session, models.User, user_id)
    
    # Проверяем права: только admin или сам пользователь
    if token.user.role != 'admin' and user_orm_obj.id != token.user_id:
        raise HTTPException(403, 'Insufficient privileges')
    
    await crud.delete_item(session, user_orm_obj)
    return SUCCESS_RESPONSE

@app.post('/api/v1/user/login', tags=['user'], response_model=LoginResponse)
async def login(login_data: LoginRequest, session: SessionDependency):
    query = select(models.User).where(models.User.name == login_data.name)
    result = await session.execute(query)
    user = result.scalars().unique().first()
    
    if user is None or not check_password(login_data.password, user.password):
        raise HTTPException(401, 'Invalid credentials')
    
    token = models.Token(user_id=user.id)
    await crud.add_item(session, token)
    return token.dict









