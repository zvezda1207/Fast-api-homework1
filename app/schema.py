from pydantic import BaseModel, Field
from typing import Literal


class SuccessResponse(BaseModel):
    status: Literal['success']

class CreateAdvRequest(BaseModel):
    title: str
    description: str
    price: float = Field(gt=0)
    author: str

class UpdateAdvRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = Field(None, gt=0)
    author: str | None = None


class CreateAdvResponse(BaseModel):
    id: int

class UpdateAdvResponse(SuccessResponse):
    pass

class GetAdvResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float
    author: str
    created_at: str 

class SearchAdvResponse(BaseModel):
    results: list[GetAdvResponse]

class DeleteAdvResponse(SuccessResponse):
    pass

