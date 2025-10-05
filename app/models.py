from sqlalchemy import Integer, String, func, DateTime, Float, UUID, ForeignKey, func, text
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker, create_async_engine)
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
import datetime
import uuid

from . import config
from .custom_type import ROLE

engine = create_async_engine(config.PG_DSN)

Session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase, AsyncAttrs):
    @property
    def id_dict(self):
        return {'id': self.id}

class Token(Base):
    __tablename__ = 'token'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token: Mapped[uuid.UUID] = mapped_column(UUID, unique=True, server_default=func.gen_random_uuid())
    creation_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship('User', back_populates='tokens')

    @property
    def dict(self):
        return {'token': self.token}

class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    role: Mapped[ROLE] = mapped_column(String, default='user')
    tokens: Mapped[list['Token']] = relationship('Token', lazy='joined', back_populates='user')
    advs: Mapped[list['Adv']] = relationship('Adv', lazy='joined', back_populates='user')

    @property
    def dict(self):
        return {'id': self.id, 'name': self.name, 'role': self.role}

class Adv(Base):
    __tablename__ = 'adv'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    author: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship('User', lazy='joined', back_populates='advs')

    @property
    def dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'author': self.author,
            'created_at': self.created_at.isoformat(),
            'user_id': self.user_id,
        }
    
ORM_OBJ = Adv | User | Token
ORM_CLS = type[Adv] |type[User] | type[Token]

# async def init_orm():
#     print('INIT ORM STARTING')
#     async with engine.begin() as conn:
#         print("Creating tables...")
#         await conn.run_sync(Base.metadata.create_all)
#         print("Tables created.")

async def init_orm():
    print("INIT ORM STARTING")
    async with engine.begin() as conn:
        print("Checking database connection...")
        await conn.execute(text("SELECT 1"))  # Оберните строку в text()
        print("Creating tables...")
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created.")

async def close_orm():
    await engine.dispose() 