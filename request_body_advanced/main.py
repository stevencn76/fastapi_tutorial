from enum import Enum
from typing import Optional, List, Set

import uvicorn
from fastapi import FastAPI, Path, Query, Body
from pydantic import BaseModel, Field


app = FastAPI()


class Address(BaseModel):
    address: str
    postcode: str


class User(BaseModel):
    username: str = Field(..., min_length=3)
    description: Optional[str] = Field(None, max_length=10)
    address: Address


class Feature(BaseModel):
    name: str


class Item(BaseModel):
    name: str
    length: int
    features: List[Feature]


@app.put('/carts/{cart_id}')
async def update_cart(cart_id: int, user: User, item: Item, count: int = Body(..., ge=2)):
    print(user.username)
    print(item.name)
    result_dict = {
        "cartid": cart_id,
        "username": user.username,
        "itemname": item.name,
        "count": count
    }

    return result_dict


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
