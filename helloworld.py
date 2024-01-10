import uvicorn
from fastapi import FastAPI


app = FastAPI()


@app.get('/')
async def hello_world2():
    return {'message': 'Hello World 2'}


@app.get('/helloworld')
async def hello_world():
    return {'message': 'Hello World'}


if __name__ == '__main__':
    uvicorn.run("helloworld:app", reload=True)
