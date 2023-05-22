from fastapi import FastAPI
import pandas as pd
from pymongo import mongo_client
import pydantic
from bson.objectid import ObjectId
import os.path
import json
import chardet

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
secret_file = os.path.join(BASE_DIR, '../secret.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        errorMsg = "Set the {} environment variable.".format(setting)
        return errorMsg

HOSTNAME = get_secret("ATLAS_Hostname")
USERNAME = get_secret("ATLAS_Username")
PASSWORD = get_secret("ATLAS_Password")

client = mongo_client.MongoClient(f'mongodb+srv://{USERNAME}:{PASSWORD}@{HOSTNAME}')
print('Connected to Mongodb....')

mydb = client['test']
mycol = mydb['projectdb']

@app.get('/')
def healthCheck():
    return "OK"

@app.get('/getmongo')
async def getMongo():
    return list(mycol.find())

@app.get('/getdata')
async def getdate(dataDate=None):
    if getdate is None:
        return "'년도-월-일'을 입력하세요"
    result = mycol.find_one({"dataDate":dataDate})
    if result:
        return result
    else:
        return "검색 결과가 없습니다."

@app.get('/add_data')
async def add_data():
    for year in range(2018,2023):
        with open(f"xx_ultrafine_{year}.json", "r") as file:
            data = json.load(file)

        for item in data:
            mycol.insert_one(item)

        return "데이터가 추가되었습니다."