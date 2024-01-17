from enum import Enum
from typing import Optional, List, Set, Union

import uvicorn
from fastapi import FastAPI, Path, Query, Body, Cookie, Header, Response
from pydantic import BaseModel, Field


app = FastAPI()


@app.put('/carts')
async def update_cart(*,
                      response: Response,
                      favorite_schema: Optional[str] = Cookie(None, alias="favorite-schema"),
                      api_token: Union[str, None] = Header(None, alias="api-token")):
    result_dict = {
        "favorite_schema": favorite_schema,
        "api_token": api_token
    }

    response.set_cookie(key="favorite-schema", value="dark")

    return result_dict


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
