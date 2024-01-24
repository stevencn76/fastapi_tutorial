from datetime import timedelta, timezone, datetime
from typing import Optional, List, Set, Union

import jwt
import uvicorn
from fastapi import FastAPI, Path, Query, Body, Cookie, Header, Request, Response, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, String, Integer, select
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column


SECURITY_KEY = "ioweurlaksjdfoiquwerlkasjdf"
ALGORITHMS = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


class Token(BaseModel):
    access_token: str
    token_type: str


app = FastAPI()


def validate_user(username: str, password: str):
    if username == 'jack' and password == '111':
        return username

    return None


def get_current_username(token: str = Depends(oauth2_scheme)):
    unauth_exp = HTTPException(status_code=401, detail="Unauthorized")
    try:
        username = None
        token_data = jwt.decode(token, SECURITY_KEY, ALGORITHMS)
        if token_data:
            username = token_data.get('username', None)
    except Exception as error:
        raise unauth_exp

    if not username:
        raise unauth_exp

    return username


@app.post('/token')
async def login(login_form: OAuth2PasswordRequestForm = Depends()):
    username = validate_user(login_form.username, login_form.password)
    if not username:
        raise HTTPException(status_code=401,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})

    token_expires = datetime.now(timezone.utc) + timedelta(minutes=300)
    token_data = {
        "username": username,
        "exp": token_expires
    }

    token = jwt.encode(token_data, SECURITY_KEY, ALGORITHMS)
    return Token(access_token=token, token_type="bearer")


@app.get('/items')
async def get_items(username: str = Depends(get_current_username)):
    return {"current user": username}


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
