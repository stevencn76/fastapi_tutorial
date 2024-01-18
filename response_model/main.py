from enum import Enum
from typing import Optional, List, Set, Union

import uvicorn
from fastapi import FastAPI, Path, Query, Body, Cookie, Header, Response
from pydantic import BaseModel, Field


users = {
    # "x": {"id": 0},
    "a": {"id": 1, "username": "a"},
    "b": {"id": 2, "username": "b", "password": "bbb"},
    "c": {"id": 3, "username": "c", "password": "ccc", "description": "default"},
    "d": {"id": 4, "username": "d", "password": "ddd", "description": "user ddd"},
    "e": {"id": 5, "username": "e", "password": "eee", "description": "user eee", "fullname": "Mary Water"}
}

app = FastAPI()


class UserOut(BaseModel):
    id: int
    username: str
    description: Optional[str] = "default"


# response_model_exclude={"id"}
# response_model_include={"id", "username"}
@app.get('/users/{username}', response_model=UserOut, response_model_exclude_unset=True)
async def get_user(username: str):
    return users.get(username, {})


@app.get('/users', response_model=List[UserOut])
async def get_users():
    return users.values()


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
