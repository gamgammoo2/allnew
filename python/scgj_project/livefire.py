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
mycol = mydb['livefiredb']

def getRequestUrl(url):
    req = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            return response.read().decode('utf-8')
    except Exception as e:
        return None

def livetemp():
    url = 'http://192.168.1.187:5000/sanbul'

    result = getRequestUrl(url)

    if (result == None):
        return None
    else:
        return json.loads(result)

#월별필드를 기준으로 입력되는 중복되는 데이터를 검색하기
def duplica(city,st):
    query = {"Unnamed: 10":city,"Unnamed: 3":st}
    count = mycol.count_documents(query)
    return count > 0

#연결 체크
@app.get('/')
def healthCheck():
    return {"OK":True}

#월별 산불 발생수가 mongodb에 저장됨(중복 안되게 처리)
@app.get('/add_livefire')
async def save_data_livefire_mongo():
    listResult = []
    listData = livetemp()
    for item in listData:
        if not duplica(item["Unnamed: 10"],item["Unnamed: 3"]):
            listResult.append(item)
    
    if listResult:
        mycol.insert_many(listResult)
    # return "데이터 추가되었습니다."
    return {"OK": True, "db": "mongodb", "service": "/add_livefire"}

from collections import defaultdict
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

#mongodb에 저장된 모든 데이터 가져오기
@app.get('/livefiremongo')
async def livefiremongo():
    result=list(mycol.find({"년도별 산불통계": {"$eq": "2023"}}))#리스트의안의 딕셔너리에서 "년도별 산불통계"키의 값이 "2023"인 것들만 들고와야함
    dict_result={}
    
    # collections 모듈의 defaultdict을 사용하여 딕셔너리의 초기값을 0으로 설정
    dict_result = defaultdict(int)

    for data in result:
        key = f'{data["년도별 산불통계"]}-{data["Unnamed: 1"]}'
        dict_result[key] += 1
    data=dict(dict_result)

    # 데이터프레임 생성
    df = pd.DataFrame(data.items(), columns=["Key", "Value"])
    df = df.sort_values("Key")

    # 그래프 생성
    plt.figure(figsize=(15, 9))
    plt.scatter(df["Key"], df["Value"], color="b", label="Data")

    # 선형 회귀 모델 학습
    X = np.arange(len(df)).reshape(-1, 1)
    y = df["Value"].values.reshape(-1, 1)
    reg = LinearRegression()
    reg.fit(X, y)

    # 추세선 그리기
    plt.plot(df["Key"], reg.predict(X), color="r", label="Trendline")

    # R² 값 계산
    r2 = r2_score(y, reg.predict(X))
    r2_label = f"R² = {r2:.2f}"

    # R² 값 표시
    plt.text(0.5, df["Value"].max() - 0.5, r2_label, ha="center", va="bottom", color="g")

    # 그래프 스타일 및 레이블 설정
    plt.xticks(rotation=45)
    plt.xlabel("Key")
    plt.ylabel("Value")
    plt.title("Graph with Trendline and R² Value")
    plt.legend()

    plt.savefig(f"livefire.png", dpi=400, bbox_inches='tight')

    return data,f"livefire.png saved..."
    # return {"OK": True, "db": "mongodb", "service": "/livefiremongo"}
