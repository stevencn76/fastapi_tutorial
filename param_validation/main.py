from enum import Enum

import uvicorn
from fastapi import FastAPI, Path, Query


app = FastAPI()


@app.get('/users')
async def get_users(page_index: int = Query(1, alias='page-index', title='Page Index', ge=1, le=1000)):
    return {'user': f'Index: {page_index}'}


@app.get('/users/{user_id}')
async def get_user(user_id: int = Path(..., title='User ID', ge=1, le=1000)):
    return {'user': f'This is the user for {user_id}'}


@app.get('/books/{book_name}')
async def get_book(book_name: str = Path(..., title='Book Name', min_length=3, max_length=10)):
    return {'Book Info': f'This is a book for {book_name}'}


@app.get('/items/{item_no}')
async def get_item(item_no: str = Path(..., title='Item No', regex='^[a|b|c]-[\\d]*$')):
    return {'Item Info': f'This is an item for {item_no}'}


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
