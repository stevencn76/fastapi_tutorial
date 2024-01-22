from enum import Enum
from typing import Optional, List, Set, Union

import uvicorn
from fastapi import FastAPI, Path, Query, Body, Cookie, Header, Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
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


class UserBase(BaseModel):
    id: Optional[int] = None
    username: str
    fullname: Optional[str] = None
    description: Optional[str] = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    ...


class ErrorMessage(BaseModel):
    error_code: int
    message: str


class UserNotFoundException(Exception):
    def __init__(self, username: str):
        self.username = username


@app.post('/users', status_code=201, response_model=UserOut, responses={
    400: {'model': ErrorMessage},
    401: {'model': ErrorMessage}
})
async def create_user(user: UserIn):
    if users.get(user.username, None):
        error_message = ErrorMessage(error_code=400, message=f'{user.username} already exists')
        return JSONResponse(status_code=400, content=error_message.model_dump())

    user_dict = user.model_dump()
    user_dict.update({"id": 10})

    return user_dict


@app.get('/users/{username}', status_code=200, response_model=UserOut)
async def get_user(username: str = Path(..., min_length=1)):
    user = users.get(username, None)
    if user:
        return user

    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{username} not found')
    raise UserNotFoundException(username)


@app.exception_handler(UserNotFoundException)
async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(status_code=404, content={
        'error_code': 404,
        'message': f'{exc.username} not found',
        'info': 'alskdfjaslfdkj'
    })

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
