from fastapi import FastAPI
from pydantic import BaseModel
from database import db_conn
from models import St_info, St_grade

app = FastAPI()

db = db_conn()
session = db.sessionmaker()

#basemodel 왜만드냐면 post방식으로 파라메터를 전달할때 필요함/get에서는 필없음
class Item(BaseModel):
    name:str
    number : int

@app.get('/')
async def healthCheck():
    return "OKAY"
    
@app.get('/stinfo')
async def select_st_info():
    result=session.query(St_info)
    return result.all()

@app.get('/stgrade')
async def select_st_grade():
    result=session.query(St_grade)
    return result.all()

@app.get('/getuser')
async def getuser(id=None, name=None):
    if (id is None) and (name is None):
        return "학번 또는 아이디 검색하쇼"
    else:
        if name is None:
            result = session.query(St_info).filter(St_info.ST_ID == id).all()
        elif id is None:
            result = session.query(St_info).filter(St_info.NAME == name).all()
        else:
            result = session.query(St_info).filter(St_info.ST_ID == id, St_info.NAME == name).all()
        return result

@app.get('/useradd')
async def useradd(id=None, name=None, dept=None):
    if (id and name and dept) is None:
        return "학번이랑 아이디랑 학과 넣으쇼"
    else:
        user = St_info(ST_ID=id,NAME=name,DEPT=dept)
        session.add(user)
        session.commit()
        result=session.query(St_info).all()
        return result
        
@app.get("/userupdate")
async def updateadd(id=None, name=None, dept=None):
    if id is None:
        return "학번을 입력하세요"
    else:
        user = session.query(St_info).filter(St_info.ST_ID == id).first()
        user.NAME = name
        user.DEPT = dept
        session.add(user)
        session.commit()
        result = session.query(St_info).filter(St_info.ST_ID == id).all()
        return result

@app.get("/userdel")
async def updateadd(id=None):
    if id is None:
        return "학번을 입력하세요"
    else:
        session.query(St_info).filter(St_info.ST_ID == id).delete()
        session.commit()
        result = session.query(St_info).all()
        return result
