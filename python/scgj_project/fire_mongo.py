import json, urllib.request
import os.path
from pymongo import mongo_client

from fastapi import FastAPI
import pandas as pd
import numpy as np
import pydantic
from bson.objectid import ObjectId
import matplotlib.pyplot as plt  

plt.rcParams['font.family'] = "AppleGothic"

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
mycol = mydb['firedb']

def getRequestUrl(url):
    req = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            return response.read().decode('utf-8')
    except Exception as e:
        return None

def fire():
    url = 'http://192.168.1.187:5000/fire'

    result = getRequestUrl(url)

    if (result == None):
        return None
    else:
        return json.loads(result)

#월별필드를 기준으로 입력되는 중복되는 데이터를 검색하기
def duplica(mth):
    query = {"월별":mth}
    count = mycol.count_documents(query)
    return count > 0

#연결 체크
@app.get('/')
def healthCheck():
    return {"OK":True}

#년도별 산불 발생수가 mongodb에 저장됨(중복 안되게 처리)
@app.get('/add_fire')
async def save_data_fire_mongo():
    listResult = []
    listData = fire()
    for item in listData:
        if not duplica(item["월별"]):
            listResult.append(item)
    
    if listResult:
        mycol.insert_many(listResult)
    return "데이터 추가되었습니다."

#mongodb에 저장된 모든 데이터 가져오기
@app.get('/firemongo')
async def firemongo():
    result=list(mycol.find())[1:]#리스트의 첫번째 dict는 총합이라서 두번째부터 들고와야함
    dict_result={}

    for data in result:
        years = {year: data[year] for year in ["2018","2019","2020","2021","2022"]}
        values = {f'{year}-{str(data["월별"].replace("월","")).zfill(2)}':str(count) for year, count in years.items()}
        dict_result.update(values)

    return dict_result

#mongodb에 저장된 입력한 년도에 맞아떨어지는 데이터 가져오기
@app.get('/year_firemongo')
async def year_firemongo(year=None):
    if year is None:
        return "'년도(ex,2018)의 입력을 확인해주세요"
    else:
        result=await firemongo()
        data = {key:value for key, value in result.items() if key.split('-')[0] == year}
        return data
    
#mongodb에 저장된 입력한 년도중 하반기 데이터 가져오기
@app.get('/month_firemongo')
async def month_firemongo(year=None):
    if year is None:
        return "'년도(ex,2018)의 입력을 확인해주세요"
    else:
        months=["06","07","08","09","10","11","12"]
        result=await firemongo()
        data = {key:value for key, value in result.items() if key.split('-')[0] == year and key.split('-')[1] in months}
        return data
    
