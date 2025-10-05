import datetime
from typing import Annotated
import uuid
from fastapi import Depends, HTTPException, Header
from fastapi import Depends
from .models import Session, Token
from .config import TOKEN_TTL_SEC
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

async def get_session() -> AsyncSession:
    async with Session() as session:
        yield session

SessionDependency = Annotated[AsyncSession, Depends(get_session, use_cache=True)]

async def get_token(x_token: Annotated[uuid.UUID, Header()], session: SessionDependency) -> Token:
    query = select(Token).where(
        Token.token == x_token, 
        Token.creation_time >= (datetime.datetime.now() - datetime.timedelta(seconds=TOKEN_TTL_SEC))
    )

    result = await session.execute(query)
    token = result.scalars().unique().first()
    if token is None:
        raise HTTPException(401, 'Token not found')
    
    return token

TokenDependency = Annotated[Token, Depends(get_token)]

async def get_optional_token(x_token: Optional[uuid.UUID] = Header(None), session: SessionDependency = None) -> Optional[Token]:
    if x_token is None or session is None:
        return None
    
    query = select(Token).where(
        Token.token == x_token, 
        Token.creation_time >= (datetime.datetime.now() - datetime.timedelta(seconds=TOKEN_TTL_SEC))
    )

    result = await session.execute(query)
    token = result.scalars().unique().first()
    return token

OptionalTokenDependency = Annotated[Optional[Token], Depends(get_optional_token)]
