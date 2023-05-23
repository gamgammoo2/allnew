from fastapi import FastAPI
import pandas as pd
import numpy as np
from pymongo import mongo_client
import pydantic
from bson.objectid import ObjectId
import os.path
import json
from uf2 import save_data_to_mongodb
import re
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
mycol = mydb['projectdb']

#연결 체크
@app.get('/')
def healthCheck():
    return "OK"

#몽고db에 저장된 데이터들을 모두 가져오기
@app.get('/getmongo')
async def getMongo():
    result=list(mycol.find())
    df = pd.DataFrame(result)
    df['dataDate']=pd.to_datetime(df['dataDate'])
    df.set_index('dataDate',inplace = True)
    results = df.groupby(pd.Grouper(freq='D')).size().to_dict()
    return results

#"년도-월-일" 형식으로 입력하면, 해당 일의 경보 발생 정보를 도출
@app.get('/getdata')
async def getdate(dataDate=None):
    if getdate is None:
        return "'년도-월-일(ex,2018-01-01)'을 입력하세요"
    result = list(mycol.find({"dataDate":dataDate}))
    if result:
        return result
    else:
        return "검색 결과가 없습니다."

#년도를 입력하면 해당 년도의 초미세먼지 경보 데이터가 mongodb에 저장됨
@app.get('/add_data')
async def add_data(year=None):
    if add_data is None:
        return "년도를 입력해주세요"
    else:
        result = save_data_to_mongodb(year)
        return result

#년도를 입력하면, 09월부터 다음해 2월까지의 "월별" 초미세먼지 경보발생 수의 합을 도출
@app.get('/get_winter')
async def get_winter(year=None):
    if year is None:
        return "'년도(ex,2018)'을 입력하세요"
    else:
        months1 = ["09", "10", "11", "12"]
        months2 = ["01", "02"]
        seek=[re.compile(f"{str(year)}-{month}") for month in months1]+[re.compile(f"{int(year)+1}-{month}") for month in months2]
        query = {"dataDate" : {"$in":seek}}
        cursor = mycol.find(query)

        data = {}
        for item in cursor:
            dataDate = item["dataDate"]
            if dataDate[:7] not in data:
                data[dataDate[:7]] = 1
            else:
                data[dataDate[:7]] += 1
       
        df = pd.DataFrame({"dataDate": list(data.keys()), "count": list(data.values())})
        df.set_index("dataDate", inplace=True)
        df.sort_index(inplace=True)

        df.plot(kind='bar',rot=0,ylim=[0, df['count'].max()+10],use_index=True,grid=False,table=False,figsize=(20, 12))

        plt.xlabel("년도-월")
        plt.ylabel("발생 수")
        plt.title(f"{year}년도의 가을,겨울 초미세먼지 경보 발생 수")

        for idx in range(df['count'].size):
            value = str(df['count'][idx]) + '건'
            plt.text(x=idx,y=df['count'][idx]+1,s=value, horizontalalignment='center')

        colors = ['#ffab91', '#ffe082', '#c5e1a5', '#80cbc4', '#81d4fa', '#b39ddb']
        plt.bar(df.index, df['count'], color=colors)

        filename=f'ultrafine_2half_{year}.png'
        plt.savefig(filename, dpi=400, bbox_inches='tight')

        plt.show()
        return(filename +'  saved..')

#년도를 입력시, 해당년도의 월별 초미세먼지의 경보수 합산
@app.get('/get_total')
async def get_total(year=None):
    if year is None:
        return "'년도(ex,2018)'을 입력하세요"
    else:
        seek=[re.compile(f"{str(year)}-{str(month).zfill(2)}") for month in range(1,13)]
        query = {"dataDate" : {"$in":seek}}
        cursor = mycol.find(query)

        data = {}
        for item in cursor:
            dataDate = item["dataDate"]
            if dataDate[:7] not in data:
                data[dataDate[:7]] = 1
            else:
                data[dataDate[:7]] += 1

        #data에서 없는 월을 value를 0으로 채워넣기
        for months in range(1, 13):
            month_str = str(months).zfill(2)
            date_str = f"{str(year)}-{month_str}"
            if date_str not in data:
                data[date_str] = 0
       
        df = pd.DataFrame({"dataDate": list(data.keys()), "count": list(data.values())})
        df.set_index("dataDate", inplace=True)
        df.sort_index(inplace=True)

        df.plot(kind='bar',rot=0,ylim=[0, df['count'].max()+10],use_index=True,grid=False,table=False,figsize=(20, 12))

        plt.xlabel("년도-월")
        plt.ylabel("발생 수")
        plt.title(f"{year}의 초미세먼지 경보 발생 수")

        for idx in range(df['count'].size):
            value = str(df['count'][idx]) + '건'
            plt.text(x=idx,y=df['count'][idx]+1,s=value, horizontalalignment='center')

        colors = ['#ffab91', '#ffcc80', '#ffe082', '#e6ee9c', '#c5e1a5', '#a5d6a7', '#80cbc4', '#80deea', '#81d4fa', '#90caf9', '#9fa8da', '#b39ddb']
        plt.bar(df.index, df['count'], color=colors)

        filename=f'ultrafine_total_{year}.png'
        plt.savefig(filename, dpi=400, bbox_inches='tight')

        plt.show()
        return(filename +'  saved..')
    
#지우고 싶은 년도 입력시, 해당년도 데이터 삭제
@app.get("/yeardel")
async def yeardel(year=None):
        if year is None:
            return "지우고 싶은 year을 입력하세요(ex, 2018)"
        else:
            query={"dataDate":{"$regex":f"^{year}-"}}
            mycol.delete_many(query)

            # remaining=[item for item in mycol.find()]
            return (f"{year}의 Data가 정상 삭제 되었습니다.")
        


 