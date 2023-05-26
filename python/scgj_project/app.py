from fastapi import FastAPI
import requests
from database import db_conn
from models import ufTotal, ufHalf
from uf_mongo import get_totalnum,get_monthnum
from fire_mongo import year_firemongo,month_firemongo

import pandas as pd
import numpy as np

import json

app = FastAPI()

db = db_conn()
session = db.sessionmaker()

@app.get('/')
async def healthCheck():
    return "OKAY"

#input year -> mysql
@app.get('/add_total')
async def add_total(year=None):
    if year is None:
        return "'년도(ex,2018)'을 입력하세요"
    else:
        result = await get_totalnum(year)
        #result는 딕셔너리 형태로 들어옴
        data = result
        
        total_data = zip(data.keys(), data.values())
        #딕셔너리의 키와 값으로 zip을 생성하기
        for date, count in total_data:
            total = ufTotal(DATADATE=date, COUNT=count)
            session.add(total)

        session.commit()

        results=session.query(ufTotal).all()
        
        return results

#각각의 mongodb에서 data를 들고와 dataframe을 형성하기
@app.get('/df_total')
async def df_total(year=None):
    baseurl='http://192.168.1.58:3000'
    try:
        response = requests.get(baseurl + '/gettemp?'+'year='+year)
        response.raise_for_status()
        # return response.json()
    except requests.exceptions.RequestException as e:
        return {"ok": False, "db" : "mongodb", "service" : "/month_tempmongo"}
    
    if year is None:
        return "'년도(ex,2018)'을 입력하세요"
    else:
        temp_result= response.json()
        uf_result = await get_totalnum(year)
        fire_result = await year_firemongo(year)
        #df 생성
        #'uf_result'랑 'fire_re~'가 int64로 되어있어서 오류가 발생 ->pandas의 df는 이터러블한 객체를 입력받기때문에 오류가 됌. 따라서 데이터를 dict로 변환해주어야함

        df_temp=pd.DataFrame.from_dict(temp_result, orient='index',columns=['ave_temp'])
        df_uf = pd.DataFrame.from_dict(uf_result, orient='index', columns=['alert_occur'])
        df_fire = pd.DataFrame.from_dict(fire_result, orient='index', columns=['fire_occur'])
        
        df_temp['ave_temp']=df_temp['ave_temp'].astype(str)
        df_uf['alert_occur']=df_uf['alert_occur'].astype(str)
        
        
        # 데이터프레임 병합
        #df 병합(date를 기준으로 병합, how의 outer은 모든 데이터를 포함하겠다는 것)
        df_merging = pd.merge(df_temp,df_uf,left_index=True,right_index=True)
        df_merging = pd.merge(df_merging,df_fire,left_index=True,right_index=True)

        df_merging.index.name = 'year-month'
        df_merging.columns=['temp', 'uf','fire']

        return df_merging

#각각의 시즌별(여름,가을 겨울) mongodb에서 data를 들고와 dataframe을 형성하기
@app.get('/df_season')
async def df_season(year=None):
    if year is None:
        return "'년도(ex,2018)'을 입력하세요"
    else:
        baseurl='http://192.168.1.58:3000'
        try:
            response = requests.get(baseurl + '/month_tempmongo?'+'year='+year)
            response.raise_for_status()
        # return response.json()
        except requests.exceptions.RequestException as e:
            return {"ok": False, "db" : "mongodb", "service" : "/month_tempmongo"}
        temp_result= response.json()
        uf_result = await get_monthnum(year)
        fire_result = await month_firemongo(year)
        #df 생성
        #'uf_result'랑 'fire_re~'가 int64로 되어있어서 오류가 발생 ->pandas의 df는 이터러블한 객체를 입력받기때문에 오류가 됌. 따라서 데이터를 dict로 변환해주어야함

        df_temp=pd.DataFrame.from_dict(temp_result, orient='index',columns=['ave_temp'])
        df_uf = pd.DataFrame.from_dict(uf_result, orient='index', columns=['alert_occur'])
        df_fire = pd.DataFrame.from_dict(fire_result, orient='index', columns=['fire_occur'])

        df_temp = df_temp.fillna(0)
        df_temp['ave_temp'] = df_temp['ave_temp'].astype(str)
        df_uf = df_uf.fillna(0)
        df_uf['alert_occur'] = df_uf['alert_occur'].astype(str)
        df_fire = df_fire.fillna(0)
        df_fire['fire_occur'] = df_fire['fire_occur'].astype(str)

        df_merging = pd.concat([df_temp, df_uf, df_fire], axis=1, sort=True, join='outer')

        json_data = json.loads(df_merging.to_json(orient='index'))

        return json_data

#request test
#yeonji's temp average data import
@app.get('/yeonjimongo')
async def tempmongo():
    baseurl = 'http://192.168.1.58:3000'
    try:
        response = requests.get(baseurl + '/tempmongo')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"ok": False, "db" : "mongodb", "service" : "/tempmongo"}
    