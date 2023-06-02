from fastapi import FastAPI,File, UploadFile
import pandas as pd
import numpy as np
from pymongo import mongo_client
import pydantic
from bson.objectid import ObjectId
import os.path
import json
from uf2 import save_data_to_mongodb
import re #re.compile을 하기위해서 필요
import matplotlib.pyplot as plt  

from fastapi.encoders import jsonable_encoder

#mysql--
import requests
from database import db_conn
from models import ufTotal,ufGraph
from sqlalchemy import create_engine, text
from PIL import Image
import base64
from io import BytesIO
from typing import List
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

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

os.makedirs("./images", exist_ok=True)
app.mount("/images", StaticFiles(directory="./images"), name='images')

HOSTNAME = get_secret("Mysql_Hostname")
PORT = get_secret("Mysql_Port")
USERNAME = get_secret("Mysql_Username")
PASSWORD = get_secret("Mysql_Password")
DBNAME = get_secret("Mysql_DBname")

DB_URL = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DBNAME}'

engine = create_engine(DB_URL, pool_recycle=500)

db = db_conn()
session = db.sessionmaker()
#mysql --

#연결 체크
# @app.get('/')
# def healthCheck():
#     return {"OK":True}

#년도를 입력하면 해당 년도의 초미세먼지 경보 데이터가 mongodb에 저장됨
@app.get('/add_data')
async def add_data(year=None):
    if add_data is None:
        return {"INSERT": "OK","DB": "MongoDB","Data": f"{year}"}
    else:
        result = save_data_to_mongodb(year)
        return result
        # return {"OK": True, "db": "mongodb", "service": "/add_data"}

#몽고db에 저장된 데이터들을 column 중 dataDate부분만 경보발생수 합쳐서 가져오기
# @app.get('/getmongo')
# async def getMongo():
#     result=list(mycol.find())
#     df = pd.DataFrame(result)
#     df['dataDate']=pd.to_datetime(df['dataDate'])
#     df.set_index('dataDate',inplace = True)
#     results = df.groupby(pd.Grouper(freq='D')).size().to_dict()
#     return results

#년도를 입력하면, 05월부터 다음해 4월까지의 "월별" 초미세먼지 경보발생 수의 합을 도출 및 그래프로 시각화
@app.get('/get_winter')
async def get_winter(year1=None,year2=None):
    if year1 is None or year2 is None:
        return "'년도(ex,2018)'을 입력하세요"
    else:
        months1 = ["05","06","07","08","09", "10", "11", "12"]
        months2 = ["01", "02","03","04"]
        seek1=[re.compile(f"{str(year1)}-{month}") for month in months1]+[re.compile(f"{int(year1)+1}-{month}") for month in months2]
        seek2=[re.compile(f"{str(year2)}-{month}") for month in months1]+[re.compile(f"{int(year2)+1}-{month}") for month in months2]
        query1 = {"dataDate" : {"$in":seek1}}
        query2={"dataDate" : {"$in":seek2}}
        cursor1 = mycol.find(query1)
        cursor2 = mycol.find(query2)
        
        cursor1_list = list(cursor1)
        cursor2_list = list(cursor2)
        cursor = cursor1_list + cursor2_list

        data_dict = {}
        for item in cursor:
            dataDate = item["dataDate"]
            if dataDate[:7] not in data_dict:
                data_dict[dataDate[:7]] = 1
            else:
                data_dict[dataDate[:7]] += 1

        #data에서 없는 월을 값을 0으로 채워넣기
        for months in months1:
            date_str1 = f"{str(year1)}-{months}"
            date_str2 =  f"{str(year2)}-{months}"
            if date_str1 not in data_dict:
                data_dict[date_str1] = 0
            if date_str2 not in data_dict:
                data_dict[date_str2] = 0

        for monthss in months2:
            date_str1 = f"{str(int(year1)+1)}-{monthss}"
            date_str2 =  f"{str(int(year2)+1)}-{monthss}"
            if date_str1 not in data_dict:
                data_dict[date_str1] = 0
            if date_str2 not in data_dict:
                data_dict[date_str2] = 0

        result = [{"년도-월": key, "초미세먼지 경보 수": str(value) } for key, value in data_dict.items()]

        df = pd.DataFrame(result, columns = ['년도-월','초미세먼지 경보 수'])
        
        # '년월' 열을 날짜형으로 변환
        df['년도-월'] = pd.to_datetime(df['년도-월'])
        
        # 입력한 연도 데이터 필터링
        df_year1 = df[((df['년도-월'].dt.year == int(year1)) & (df['년도-월'].dt.month >= 5)) + ((df['년도-월'].dt.year == int(year1) + 1) & (df['년도-월'].dt.month <= 4))].sort_values(by='년도-월')
        df_year2 = df[((df['년도-월'].dt.year == int(year2)) & (df['년도-월'].dt.month >= 5)) + ((df['년도-월'].dt.year == int(year2) + 1) & (df['년도-월'].dt.month <= 4))].sort_values(by='년도-월')


        # '년도-월' 열의 형식을 월만 짜르기
        df_year1['년도-월'] = df_year1['년도-월'].dt.strftime('%Y-%m')
        df_year2['년도-월'] = df_year2['년도-월'].dt.strftime('%Y-%m')
        
        # #df의 index를 바꿔야함
        # df_json1 = jsonable_encoder(df_year1.reset_index(drop=True))
        # df_json2 = jsonable_encoder(df_year2.reset_index(drop=True))
    
        # 그래프 그리기
        fig, ax = plt.subplots(figsize=(10, 6))

        # 입력한 연도 데이터에서 월별 데이터 추출
        x1 = df_year1['년도-월'].str[-2:].tolist()
        y1 = df_year1['초미세먼지 경보 수'].astype(int).tolist()
        x2 = df_year2['년도-월'].str[-2:].tolist()
        y2 = df_year2['초미세먼지 경보 수'].astype(int).tolist()

        # 입력한 연도 그래프 그리기
        ax.plot(x1, y1, marker='o', label=str(year1) + '년', color='lightpink')
        ax.plot(x2, y2, marker='x', label=str(year2) + '년', color='steelblue')

        ax.set_xlabel('월')
        ax.set_ylabel('초미세먼지 경보 수')
        ax.set_title(str(year1) + '년 vs. ' + str(year2) + '년 월별 초미세먼지 경보 수')
        ax.legend()

        # x축 눈금 만들기
        ax.set_xticks(range(0, 12))
        ax.set_xticklabels(['05월', '06월', '07월', '08월', '09월', '10월', '11월', '12월','01월', '02월', '03월', '04월'])

        # y축 범위 지정하기
        ax.set_ylim([0, max(max(y1), max(y2)) + 10])

        # 그래프 점의 왼쪽에 값 출력
        for idx, value in enumerate(y1):
            if x1[idx] in ['09', '10', '11', '12', '01', '02']:
                plt.text(x=x1[idx], y=y1[idx]+2, s=str(value), horizontalalignment='right', verticalalignment='center', color='crimson', fontsize=15, fontweight='bold')
            else:
                plt.text(x=x1[idx], y=y1[idx]+1, s=str(value), color='lightpink', horizontalalignment='right', verticalalignment='center')

        # 그래프의 점 오른쪽에 값 출력
        for idx, value in enumerate(y2):
            if x2[idx] in ['09', '10', '11', '12', '01', '02']:
                plt.text(x=x2[idx], y=y2[idx]+2, s=str(value), horizontalalignment='left', verticalalignment='center', color='slateblue', fontsize=15, fontweight='bold')
            else:
                plt.text(x=x2[idx], y=y2[idx]+1, s=str(value), color='steelblue', horizontalalignment='left', verticalalignment='center')

        save_path =f'./graph/ultrafine/ultrafine_{year1}&{year2}.png'
        plt.savefig(save_path, dpi=400, bbox_inches='tight')

        return  df_year1,df_year2
        # return {"ok": True, "db": "mongodb", "service": "/get_winter"}


@app.get('/combined_frame3/{year1}/{year2}')
async def combined_frame3(year1: int, year2: int):
    df_year1, df_year2 = await get_winter(year1,year2)

    # df_year1과 df_year2를 엮기 위해 pd.concat() 함수 사용
    combined_df = pd.concat([df_year1, df_year2], axis=0, ignore_index=True)

    combined_list = []
    df1 = pd.DataFrame(combined_df)
    df2 = pd.DataFrame(combined_df)

    df1 = df1.iloc[:12]  # year1 데이터
    df2 = df2.iloc[12:]  # year2 데이터

    combined_list.append(df1.to_dict())
    combined_list.append(df2.to_dict())

    # 결과 출력
    return combined_list

#결과 도출 줄글
@app.get('/result_uf')
async def result_uf(year1=None,year2=None):
    if year1 is None or year2 is None:
        return "'년도(ex,2018)의 입력을 확인해주세요"
    else:
        months1 = ["09", "10", "11", "12"]
        months2 = ["01", "02"]

        async def get_month_data(year):
            seek1=[re.compile(f"{str(year)}-{month}") for month in months1]+[re.compile(f"{int(year)+1}-{month}") for month in months2]
         
            query1 = {"dataDate" : {"$in":seek1}}
         
            cursor1 = mycol.find(query1)
            
        
            cursor1_list = list(cursor1)
           
            cursor = cursor1_list

            data_dict = {}
            for item in cursor:
                dataDate = item["dataDate"]
                if dataDate[:7] not in data_dict:
                    data_dict[dataDate[:7]] = 1
                else:
                    data_dict[dataDate[:7]] += 1

            #data에서 없는 월을 value를 0으로 채워넣기
            for months in months1:
                date_str1 = f"{str(year)}-{months}"
                
                if date_str1 not in data_dict:
                    data_dict[date_str1] = 0
                            
            data=data_dict
            return data
    
    data1 = await get_month_data(year1)
    data2 = await get_month_data(year2)
    
    output = ""

    if data1:
        max_uf1 = max(data1.values())
        avg_uf1 = sum(data1.values()) / len(data1)
        max_month1 = [k for k, v in data1.items() if v == max_uf1][0].split('-')[1]
        output += f"{year1}년의 가을,겨울(금년 9월~후년 2월) 중 가장 '초미세먼지 경보 수'가 높은 달은 '{max_uf1}회'인 {max_month1}월입니다. {year1}년 가을,겨울(금년 9월~후년 2월)의 평균 '초미세먼지 경보 수'는 {avg_uf1:.1f}입니다.\n"

    if data2:
        max_uf2 = max(data2.values())
        avg_uf2 = sum(data2.values()) / len(data2)
        max_month2 = [k for k, v in data2.items() if v == max_uf2][0].split('-')[1]
        output += f"{year2}년의 가을,겨울(금년 9월~후년 2월) 중 가장 '초미세먼지 경보 수'가 높은 달은 '{max_uf2}회'인 {max_uf2}월입니다. {year2}년 가을,겨울(금년 9월~후년 2월)의 평균 '초미세먼지 경보 수'는 {avg_uf2:.1f}입니다."
    
    if avg_uf1 > avg_uf2:
        output += f"{year1}년의 가을,겨울에 '초미세먼지 경보 수'가 {year2}년의 가을,겨울보다 더 많았습니다."

    if avg_uf1 < avg_uf2:
        output += f"{year2}년의 가을,겨울에 '초미세먼지 경보 수'가  {year1}년의 가을,겨울보다 더 만았았습니다."

    return output

def InsertImageDB(filename):
    os.chdir('./images')
## jpg dpi 100x100, png dpi 72x72
    with open(filename, "rb") as image_file:
        binary_image = image_file.read()
        binary_image = base64.b64encode(binary_image)
        binary_image = binary_image.decode('UTF-8')
        img_df = pd.DataFrame({'filename':filename,'image_data':[binary_image]})
        #이미지의 텍스트화가 너무 길어서 longtext를 받을 수 있게 type 재정의
        with engine.begin() as connection:
            alter_query = text("ALTER TABLE images MODIFY image_data LONGTEXT")
            connection.execute(alter_query)

        # 중복 체크 후 데이터 삽입
        existing_filenames = pd.read_sql_table('images', con=engine, columns=['filename'])
        if filename in existing_filenames.values:
            return f'"OK":False,"{filename}":"exist"'
        else:
            img_df.to_sql('images', con=engine, if_exists='append', index=False)

    os.chdir('../')
    return '"Image file" : "Inserted"'

# def SelectImageDB(year1:int, year2:int):
#     with engine.connect() as conn:
#         query = text("SELECT * FROM images WHERE filename = :filename")
#         result = conn.execute(query, {"filename": f"ultrafine_{year1}&{year2}.png"})
#         result_dict=[]
#         for row in result:
#             result_dict.append(row)
        
#     return result_dict

@app.get('/for_ufgraph')
async def for_ufgraph(year1=None,year2=None):
    if year1 is None or year2 is None:
        return "'년도(ex,2018)'을 입력하세요"
    else:
        months1 = ["05","06","07","08","09", "10", "11", "12"]
        months2 = ["01", "02","03","04"]
        seek1=[re.compile(f"{str(year1)}-{month}") for month in months1]+[re.compile(f"{int(year1)+1}-{month}") for month in months2]
        seek2=[re.compile(f"{str(year2)}-{month}") for month in months1]+[re.compile(f"{int(year2)+1}-{month}") for month in months2]
        query1 = {"dataDate" : {"$in":seek1}}
        query2={"dataDate" : {"$in":seek2}}
        cursor1 = mycol.find(query1)
        cursor2 = mycol.find(query2)
        
        cursor1_list = list(cursor1)
        cursor2_list = list(cursor2)
        cursor = cursor1_list + cursor2_list

        data_dict = {}
        for item in cursor:
            dataDate = item["dataDate"]
            if dataDate[:7] not in data_dict:
                data_dict[dataDate[:7]] = 1
            else:
                data_dict[dataDate[:7]] += 1

        #data에서 없는 월을 value를 0으로 채워넣기
        for months in months1:
            date_str1 = f"{str(year1)}-{months}"
            date_str2 =  f"{str(year2)}-{months}"
            if date_str1 not in data_dict:
                data_dict[date_str1] = 0
            if date_str2 not in data_dict:
                data_dict[date_str2] = 0

        for monthss in months2:
            date_str1 = f"{str(int(year1)+1)}-{monthss}"
            date_str2 =  f"{str(int(year2)+1)}-{monthss}"
            if date_str1 not in data_dict:
                data_dict[date_str1] = 0
            if date_str2 not in data_dict:
                data_dict[date_str2] = 0

        result = [{"년도-월": key, "초미세먼지 경보 수": str(value) } for key, value in data_dict.items()]

        df = pd.DataFrame(result, columns = ['년도-월','초미세먼지 경보 수'])
        
        # '년월' 열을 날짜형으로 변환
        df['년도-월'] = pd.to_datetime(df['년도-월'])
        
        # 입력한 연도 데이터 필터링
        df_year1 = df[((df['년도-월'].dt.year == int(year1)) & (df['년도-월'].dt.month >= 5)) + ((df['년도-월'].dt.year == int(year1) + 1) & (df['년도-월'].dt.month <= 4))].sort_values(by='년도-월')
        df_year2 = df[((df['년도-월'].dt.year == int(year2)) & (df['년도-월'].dt.month >= 5)) + ((df['년도-월'].dt.year == int(year2) + 1) & (df['년도-월'].dt.month <= 4))].sort_values(by='년도-월')

        # '년도-월' 열의 형식을 월만 포함하도록 변경
        df_year1['년도-월'] = df_year1['년도-월'].dt.strftime('%Y-%m')
        df_year2['년도-월'] = df_year2['년도-월'].dt.strftime('%Y-%m')
        
        # 그래프 그리기
        fig, ax = plt.subplots(figsize=(10, 6))

        # 입력한 연도 데이터에서 월별 데이터 추출
        x1 = df_year1['년도-월'].str[-2:].tolist()
        y1 = df_year1['초미세먼지 경보 수'].astype(int).tolist()
        x2 = df_year2['년도-월'].str[-2:].tolist()
        y2 = df_year2['초미세먼지 경보 수'].astype(int).tolist()

        # 입력한 연도 그래프 그리기
        ax.plot(x1, y1, marker='o', label=str(year1) + '년', color='lightpink')
        ax.plot(x2, y2, marker='x', label=str(year2) + '년', color='steelblue')

        ax.set_xlabel('월')
        ax.set_ylabel('초미세먼지 경보 수')
        ax.set_title(str(year1) + '년 vs. ' + str(year2) + '년 월별 초미세먼지 경보 수')
        ax.legend()

        # x축 눈금 설정
        ax.set_xticks(range(0, 12))
        ax.set_xticklabels(['05월', '06월', '07월', '08월', '09월', '10월', '11월', '12월','01월', '02월', '03월', '04월'])

        # y축 범위 설정
        ax.set_ylim([0, max(max(y1), max(y2)) + 10])

        # 각 마커 왼쪽에 값 출력
        for idx, value in enumerate(y1):
            if x1[idx] in ['09', '10', '11', '12', '01', '02']:
                plt.text(x=x1[idx], y=y1[idx]+2, s=str(value), horizontalalignment='right', verticalalignment='center', color='crimson', fontsize=15, fontweight='bold')
            else:
                plt.text(x=x1[idx], y=y1[idx]+1, s=str(value), color='lightpink', horizontalalignment='right', verticalalignment='center')

        # 각 마커 오른쪽에 값 출력
        for idx, value in enumerate(y2):
            if x2[idx] in ['09', '10', '11', '12', '01', '02']:
                plt.text(x=x2[idx], y=y2[idx]+2, s=str(value), horizontalalignment='left', verticalalignment='center', color='slateblue', fontsize=15, fontweight='bold')
            else:
                plt.text(x=x2[idx], y=y2[idx]+1, s=str(value), color='steelblue', horizontalalignment='left', verticalalignment='center')

        save_path ='./images/'
        filename=f'ultrafine_{year1}&{year2}.png'
        plt.savefig(save_path+filename, dpi=400, bbox_inches='tight')
        resultss=InsertImageDB(filename)
    
        return resultss

#input year -> 년도별 경보 수  insert mysql
@app.get('/mysql_uf')
async def mysql_uf(year1=None,year2=None):
    if year1 is None and year2 is None:
        return "'년도(ex,2018,2019)'을 입력하세요"
    else:
        months1 = ["05","06","07","08","09", "10", "11", "12"]
        months2 = ["01", "02","03","04"]
        seek1=[re.compile(f"{str(year1)}-{month}") for month in months1]+[re.compile(f"{int(year1)+1}-{month}") for month in months2]
        seek2=[re.compile(f"{str(year2)}-{month}") for month in months1]+[re.compile(f"{int(year2)+1}-{month}") for month in months2]
        query1 = {"dataDate" : {"$in":seek1}}
        query2={"dataDate" : {"$in":seek2}}
        cursor1 = mycol.find(query1)
        cursor2 = mycol.find(query2)
       
        cursor1_list = list(cursor1)
        cursor2_list = list(cursor2)
        
        data_dict1 = {}
        data_dict2 = {}
        for item in cursor1_list:
            dataDate = item["dataDate"]
            if dataDate[:7] not in data_dict1:
                data_dict1[dataDate[:7]] = 1
            else:
                data_dict1[dataDate[:7]] += 1

        for item in cursor2_list:
            dataDate = item["dataDate"]
            if dataDate[:7] not in data_dict2:
                data_dict2[dataDate[:7]] = 1
            else:
                data_dict2[dataDate[:7]] += 1

        #data에서 없는 월을 value를 0으로 채워넣기
        for months in months1:
            date_str1 = f"{str(year1)}-{months}"
            if date_str1 not in data_dict1:
                data_dict1[date_str1] = 0

        for monthss in months2:
            date_str1 =  f"{str(int(year1)+1)}-{monthss}"
            if date_str1 not in data_dict1:
                data_dict1[date_str1] = 0
        
        #data에서 없는 월을 value를 0으로 채워넣기
        for months in months1:
            date_str2 =  f"{str(year2)}-{months}"
            if date_str2 not in data_dict2:
                data_dict2[date_str2] = 0

        for monthss in months2:
            date_str2 =  f"{str(int(year2)+1)}-{monthss}"
            if date_str2 not in data_dict2:
                data_dict2[date_str2] = 0

        data1 = data_dict1
        data2 = data_dict2
        
        total_data1 = zip(data1.keys(), data1.values())
        total_data2=zip(data2.keys(),data2.values())
        
        #딕셔너리의 키와 값으로 zip을 생성하기
        for (date1, count1), (date2, count2) in zip(total_data1, total_data2):
            total = ufTotal(DATADATE1=date1, COUNT1=count1, DATADATE2=date2, COUNT2=count2)
            session.add(total)
            session.dirty.add(total)

        session.commit()

        results=session.query(ufTotal).all()
        
        return results


# @app.get('/selectImages')
# async def selectImages(year1:int, year2:int):
#     result = SelectImageDB(year1,year2)
#     return result

#년도를 입력시, 해당년도의 월별 초미세먼지의 경보수와 그래프로 시각화
# @app.get('/get_total')
# async def get_total(year=None):
#     if year is None:
#         return "'년도(ex,2018)'을 입력하세요"
#     else:
#         seek=[re.compile(f"{str(year)}-{str(month).zfill(2)}") for month in range(1,13)]
#         query = {"dataDate" : {"$in":seek}}
#         cursor = mycol.find(query)

#         data = {}
#         for item in cursor:
#             dataDate = item["dataDate"]
#             if dataDate[:7] not in data:
#                 data[dataDate[:7]] = 1
#             else:
#                 data[dataDate[:7]] += 1

#         #data에서 없는 월을 value를 0으로 채워넣기
#         for months in range(1, 13):
#             month_str = str(months).zfill(2)
#             date_str = f"{str(year)}-{month_str}"
#             if date_str not in data:
#                 data[date_str] = 0
       
#         df = pd.DataFrame({"dataDate": list(data.keys()), "count": list(data.values())})
#         df.set_index("dataDate", inplace=True)
#         df.sort_index(inplace=True)

#         df.plot(kind='bar',rot=0,ylim=[0, df['count'].max()+10],use_index=True,grid=False,table=False,figsize=(20, 12))

#         plt.xlabel("년도-월")
#         plt.ylabel("발생 수")
#         plt.title(f"{year}의 초미세먼지 경보 발생 수")

#         for idx in range(df['count'].size):
#             value = str(df['count'][idx]) + '건'
#             plt.text(x=idx,y=df['count'][idx]+1,s=value, horizontalalignment='center')

#         colors = ['#ffab91', '#ffcc80', '#ffe082', '#e6ee9c', '#c5e1a5', '#a5d6a7', '#80cbc4', '#80deea', '#81d4fa', '#90caf9', '#9fa8da', '#b39ddb']
#         plt.bar(df.index, df['count'], color=colors,width=0.5)

#         filename=f'ultrafine_total_{year}.png'
#         plt.savefig(filename, dpi=400, bbox_inches='tight')

#         plt.show()
#         return data,(filename +'  saved..')
    
#지우고 싶은 년도 입력시, 해당년도 데이터 삭제
@app.get("/yeardel")
async def yeardel(year=None):
        if year is None:
            return "지우고 싶은 year을 입력하세요(ex, 2018)"
        else:
            query={"dataDate":{"$regex":f"^{year}-"}}
            mycol.delete_many(query)

            # remaining=[item for item in mycol.find()]
            return {"result": "OK"}
        

#------------------------------------------

# #년도를 입력시, 해당년도의 월별 초미세먼지의 경보수
# @app.get('/get_totalnum')
# async def get_totalnum(year=None):
#     if year is None:
#         return "'년도(ex,2018)'을 입력하세요"
#     else:
#         seek=[re.compile(f"{str(year)}-{str(month).zfill(2)}") for month in range(1,13)]
#         query = {"dataDate" : {"$in":seek}}
#         cursor = mycol.find(query)

#         data = {}
#         for item in cursor:
#             dataDate = item["dataDate"]
#             if dataDate[:7] not in data:
#                 data[dataDate[:7]] = 1
#             else:
#                 data[dataDate[:7]] += 1

#         #data에서 없는 월을 value를 0으로 채워넣기
#         for months in range(1, 13):
#             month_str = str(months).zfill(2)
#             date_str = f"{str(year)}-{month_str}"
#             if date_str not in data:
#                 data[date_str] = 0

#         sorted_data = dict(sorted(data.items()))
#         return sorted_data

# #년도를 입력시, 해당년도의 9월부터 다음해 2월까지 초미세먼지의 경보수        
# @app.get('/get_monthnum')
# async def get_monthnum(year=None):
#     if year is None:
#         return "'년도(ex,2018)'을 입력하세요"
#     else:
#         months1 = ["09", "10", "11", "12"]
#         months2 = ["01", "02"]
#         seek=[re.compile(f"{str(year)}-{month}") for month in months1]+[re.compile(f"{int(year)+1}-{month}") for month in months2]
#         query = {"dataDate" : {"$in":seek}}
#         cursor = mycol.find(query)

#         data = {}
#         for item in cursor:
#             dataDate = item["dataDate"]
#             if dataDate[:7] not in data:
#                 data[dataDate[:7]] = 1
#             else:
#                 data[dataDate[:7]] += 1

#         sorted_data = dict(sorted(data.items()))
#         return sorted_data
       

 