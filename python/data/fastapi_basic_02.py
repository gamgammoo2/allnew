from fastapi import FastAPI
from pydantic.main import BaseModel

class HelloWorldRequest(BaseModel):
    name:str
    age:str

app = FastAPI()

@app.get(path='/')
async def hello():
    return "Hello yo!!"

@app.get(path='/hello/{name}')
async def hello_with_name(name:str):
    return "Hello yo!! your name is " +name #주소창이 3000/hello/GAM -> 필수적으로 넣어야함

@app.get(path='/hello/query')
async def hello_with_querystring(name:str):
    return "Hello yo!!"+name #주소창에 3000/hello/query?name=GAM 이렇게 적어야만함

@app.post(path='/hello/post')
async def hello_post(request: HelloWorldRequest):
    return " Hellico bacter name is {}, vegiterin is {}".format(request.name, request.age)

    