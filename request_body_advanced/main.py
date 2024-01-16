from enum import Enum
from typing import Optional, List, Set

import uvicorn
from fastapi import FastAPI, Path, Query, Body
from pydantic import BaseModel, Field


app = FastAPI()


class Address(BaseModel):
    address: str = Field(..., examples=["5 Queens Street"])
    postcode: str = Field(..., examples=["0765"])

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "address": "2 Queens Street",
                "postcode": "0987"
            }]
        }
    }


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


def add(*, num1: int, num2: int):
    return num1 + num2


print(add(num1=1, num2=2))


@app.put('/carts/{cart_id}')
async def update_cart(*, cart_id: int, user: User = Body(..., examples=[{"username": "Smith"}]), item: Item, count: int = Body(..., ge=2, examples=[8])):
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
