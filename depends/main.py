from typing import Optional, List, Set, Union

import uvicorn
from fastapi import FastAPI, Path, Query, Body, Cookie, Header, Request, Response, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, String, Integer, select
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column


async def set_charset():
    print("set UTF-8")


app = FastAPI(dependencies=[Depends(set_charset)])


async def verify_auth(api_token: Optional[str] = Header(None, alias="api-token")):
    if not api_token:
        raise HTTPException(status_code=400, detail="Unauthorized")


def total_param(total_page: Optional[int] = 1):
    return total_page


def pageinfo_params(page_index: Optional[int] = 1, page_size: Optional[int] = 10,
                    total: Optional[int] = Depends(total_param)):
    return {"page_index": page_index, "page_size": page_size, "total": total}


class PageInfo:
    def __init__(self, page_index: Optional[int] = 1, page_size: Optional[int] = 10,
                 total: Optional[int] = Depends(total_param)):
        self.page_index = page_index
        self.page_size = page_size
        self.total = total


@app.get('/items')
async def get_items(page_info: dict = Depends(pageinfo_params)):

    return {"page_index": page_info.get("page_index"),
            "page_size": page_info.get("page_size"),
            "total": page_info.get("total")}


@app.get('/users', dependencies=[Depends(verify_auth)])
async def get_users(page_info: PageInfo = Depends(PageInfo)):

    return {"page_index": page_info.page_index,
            "page_size": page_info.page_size,
            "total": page_info.total}


@app.get('/goods')
async def get_users(page_info: PageInfo = Depends()):

    return {"page_index": page_info.page_index, "page_size": page_info.page_size}


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
