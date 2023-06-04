import json, urllib.request
import os.path
from pymongo import mongo_client

from fastapi import FastAPI
import pandas as pd
import numpy as np
import pydantic
from bson.objectid import ObjectId
import matplotlib.pyplot as plt  

from fastapi.encoders import jsonable_encoder

import io
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

# ---sql
import requests
from database import db_conn
from models import fireTotal
from sqlalchemy import create_engine, text
from PIL import Image
import base64
from io import BytesIO
from typing import List
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

os.makedirs("./images", exist_ok=True)
app.mount("/images", StaticFiles(directory="./images"), name='images')

HOSTNAME = get_secret("Mysql_Hostname")
PORT = get_secret("Mysql_Port")
USERNAME = get_secret("Mysql_Username")
PASSWORD = get_secret("Mysql_Password")
DBNAME = get_secret("Mysql_DBname")

DB_URL = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DBNAME}'

engine = create_engine(DB_URL, pool_recycle=500)
#mysql --


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
    # return "데이터가 추가되었습니다."
    return {"OK": True, "db": "mongodb", "service": "/add_fire"}

#mongodb에 저장된 모든 데이터 가져오기
@app.get('/firemongo')
async def firemongo():
    result=list(mycol.find({"월별":{"$ne":"합계"}}))
    #리스트의 첫번째 dict는 총합이라서 두번째부터 들고와야함
    dict_result={}

    for data in result:
        years = {year: data[year] for year in ["2018","2019","2020","2021","2022"]}
        values = {f'{year}-{str(data["월별"].replace("월","")).zfill(2)}':str(count) for year, count in years.items()}
        dict_result.update(values)

    return dict_result
    # return {"OK": True, "db": "mongodb", "service": "/firemongo"}

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

#mongodb에 저장된 입력한 년도에 맞아떨어지는 데이터 가져오기
@app.get('/year_firemongo')
async def year_firemongo(year1=None,year2=None):
    if year1 is None or year2 is None:
        return "'년도(ex,2018)의 입력을 확인해주세요"
    else:
        results=await firemongo()
        result = [{"년도-월": key, "산불 발생 수": value if value != "-" else "0"} for key, value in results.items()]

        df = pd.DataFrame(result, columns = ['년도-월','산불 발생 수'])
    
        # '년월' 열을 날짜형으로 변환
        df['년도-월'] = pd.to_datetime(df['년도-월'])

        # 입력한 연도 데이터 필터링
        df_year1 = df[df['년도-월'].dt.year == int(year1)].sort_values(by='년도-월')
        df_year2 = df[df['년도-월'].dt.year == int(year2)].sort_values(by='년도-월')

        # '년도-월' 열의 형식을 월만 포함하도록 변경
        df_year1['년도-월'] = df_year1['년도-월'].dt.strftime('%Y-%m')
        df_year2['년도-월'] = df_year2['년도-월'].dt.strftime('%Y-%m')


        #df의 index를 바꿔야함
        df_json1 = jsonable_encoder(df_year1.reset_index(drop=True))
        df_json2 = jsonable_encoder(df_year2.reset_index(drop=True))

        # 그래프 그리기
        fig, ax = plt.subplots(figsize=(10, 6))

        # 입력한 연도 데이터에서 월별 데이터 추출
        x1 = df_year1['년도-월'].str[-2:].tolist()
        y1 = df_year1['산불 발생 수'].astype(int).tolist()
        x2 = df_year2['년도-월'].str[-2:].tolist()
        y2 = df_year2['산불 발생 수'].astype(int).tolist()

        # 입력한 연도 그래프 그리기
        ax.plot(x1, y1, marker='o', label=str(year1) + '년', color='peru')
        ax.plot(x2, y2, marker='x', label=str(year2) + '년', color='darkkhaki')

        ax.set_xlabel('월')
        ax.set_ylabel('산불 발생 수')
        ax.set_title(str(year1) + '년 vs. ' + str(year2) + '년 월별 산불 발생 수')
        ax.legend()

        # x축 눈금 설정
        ax.set_xticks(range(0, 12))
        ax.set_xticklabels(['01월', '02월', '03월', '04월', '05월', '06월', '07월', '08월', '09월', '10월', '11월', '12월'])

        # y축 범위 설정
        ax.set_ylim([0, max(max(y1), max(y2)) + 10])

        #o점의  왼쪽에 값 출력
        for idx, value in enumerate(y1):
            if x1[idx] in ['06', '07', '08', '09', '10', '11', '12']:
                plt.text(x=x1[idx], y=y1[idx]+2, s=str(value), horizontalalignment='right', verticalalignment='center', color='olivedrab', fontsize=15, fontweight='bold')
            else:
                plt.text(x=x1[idx], y=y1[idx]+1, s=str(value), horizontalalignment='right', verticalalignment='center')

        # 점의오른쪽에 값 출력
        for idx, value in enumerate(y2):
            if x2[idx] in ['06', '07', '08', '09', '10', '11', '12']:
                plt.text(x=x2[idx], y=y2[idx]+2, s=str(value), horizontalalignment='left', verticalalignment='center', color='purple', fontsize=15, fontweight='bold')
            else:
                plt.text(x=x2[idx], y=y2[idx]+1, s=str(value), horizontalalignment='left', verticalalignment='center')

        save_path =f'./images/'
        filename=f'yearfire_total_{year1}&{year2}.png'
        plt.savefig(save_path+filename, dpi=400, bbox_inches='tight')
    
        return {'ok':True}

@app.get('/combined_frame2/{year1}/{year2}')
async def combined_frame2(year1: int, year2: int):
    results = await firemongo()
    
    result = [{"년도-월": key, "산불 발생 수": value if value != "-" else "0"} for key, value in results.items()]

    df = pd.DataFrame(result, columns=['년도-월', '산불 발생 수'])

    # '년월' 열을 날짜형으로 변환
    df['년도-월'] = pd.to_datetime(df['년도-월'])

    # 입력한 연도 데이터 필터링
    df_year1 = df[df['년도-월'].dt.year == int(year1)].sort_values(by='년도-월')
    df_year2 = df[df['년도-월'].dt.year == int(year2)].sort_values(by='년도-월')

    # '년도-월' 열의 형식을 월만 포함하도록 변경
    df_year1['년도-월'] = df_year1['년도-월'].dt.strftime('%Y-%m')
    df_year2['년도-월'] = df_year2['년도-월'].dt.strftime('%Y-%m')
    
    # df_year1과 df_year2를 엮기 위해 새로운 컬럼을 추가하여 값을 할당
    df_year1['Year'] = pd.to_datetime(df_year1['년도-월']).dt.year
    df_year2['Year'] = pd.to_datetime(df_year2['년도-월']).dt.year
    df_year1['Month'] = pd.to_datetime(df_year1['년도-월']).dt.month
    df_year2['Month'] = pd.to_datetime(df_year2['년도-월']).dt.month

    # df_year1과 df_year2를 엮기 위해 pd.concat() 함수 사용
    combined_df = pd.concat([df_year1, df_year2], axis=0, ignore_index=True)

    df_pivot = combined_df.pivot(index="Year", columns="Month", values="산불 발생 수")

    df_pivot = df_pivot.reindex(columns=sorted(df_pivot.columns, key=lambda x: int(x)))

    return df_pivot

#결과 도출 줄글
@app.get('/result_fire')
# 'year' 매개변수가 'None'인지 확인.
async def result_fire(year1=None,year2=None):
    if year1 is None or year2 is None:
        return "'년도(ex,2018)의 입력을 확인해주세요"
    else:
        months=["06","07","08","09","10","11","12"]

        async def get_month_data(year):
            result=await firemongo()
            data = {key:value for key, value in result.items() if key.split('-')[0] == year and key.split('-')[1] in months}
            return data
    
    data1 = await get_month_data(year1)
    data2 = await get_month_data(year2)
    
    #dictionary의 value가 "-"이면 "0"으로 대치할 수 있게 만들기
    if data1:
        data1 = {key: "0" if value == "-" else value for key, value in data1.items()}

    if data2:
        data2 = {key: "0" if value == "-" else value for key, value in data2.items()}
   
    output = ""
    
    
    if data1:
        max_fire1 = max(data1.values())
        #value의 값을 숫자로 변환
        data1_values = [int(value) for value in data1.values()]
        avg_fire1 = sum(data1_values) / len(data1_values)
        max_month1 = [k for k, v in data1.items() if v == max_fire1][0].split('-')[1]
        output += f"{year1}년의 하반기(6월~12월) 중 가장 '산불 발생 수'가 높은 달은 '{max_fire1}회'인 {max_month1}월입니다. {year1}년 하반기(6월~12월)의 평균 '산불 발생 수'는 {avg_fire1:.1f}입니다."

    if data2:
        max_fire2 = max(data2.values())
        #value의 값을 숫자로 변환
        data2_values = [int(value) for value in data2.values()]
        avg_fire2 = sum(data2_values) / len(data2_values)
        max_month2 = [k for k, v in data2.items() if v == max_fire2][0].split('-')[1]
        output += f"{year2}년의 하반기(6월~12월) 중 가장 '산불 발생 수'가 높은 달은 '{max_fire2}회'인 {max_month2}월입니다. {year2}년 하반기(6월~12월)의 평균 '산불 발생 수'는 {avg_fire2:.1f}입니다."
    if avg_fire1 > avg_fire2:
        output += f"{year1}년의 하반기에 '산불 발생 수'가 {year2}년의 하반기보다 더 많았습니다."

    if avg_fire1 < avg_fire2:
        output += f"{year2}년의 하반기에 '산불 발생 수'가 {year1}년의 하반기보다 더 많았습니다."

    return output

# db = db_conn()
# session = db.sessionmaker()

# #input year -> 년도별 경보 수  insert mysql
# @app.get('/mysql_fire')
# async def mysql_fire(year1=None,year2=None):
#     if year1 is None and year2 is None:
#         return "'년도(ex,2018,2019)'을 입력하세요"
#     else:
#         results=await firemongo()
#         result = [{"년도-월": key, "산불 발생 수": value if value != "-" else "0"} for key, value in results.items()]

#         df = pd.DataFrame(result, columns = ['년도-월','산불 발생 수'])
    
#         # '년월' 열을 날짜형으로 변환
#         df['년도-월'] = pd.to_datetime(df['년도-월'])

#         # 입력한 연도 데이터 필터링
#         df_year1 = df[df['년도-월'].dt.year == int(year1)].sort_values(by='년도-월')
#         df_year2 = df[df['년도-월'].dt.year == int(year2)].sort_values(by='년도-월')

#         # '년도-월' 열의 형식을 월만 포함하도록 변경
#         df_year1['년도-월'] = df_year1['년도-월'].dt.strftime('%Y-%m')
#         df_year2['년도-월'] = df_year2['년도-월'].dt.strftime('%Y-%m')

#         #df의 index를 바꿔야함
#         df_json1 = jsonable_encoder(df_year1.reset_index(drop=True))
#         df_json2 = jsonable_encoder(df_year2.reset_index(drop=True))

#         #딕셔너리의 키와 값으로 zip을 생성하기
#         for (date1, count1), (date2, count2) in zip(df_year1, df_year2):
#             total = fireTotal(DATADATE1=date1, COUNT1=count1, DATADATE2=date2, COUNT2=count2)
#             session.add(total)
#             session.dirty.add(total)

#         session.commit()

#         results=session.query(fireTotal).all()
        
#         return results

#람다 없이도 컬럼 정렬하기
# def convert_str_to_int(x):
#     return int(x.zfill(2))

# # df_pivot의 column sort
# df_pivot = df_pivot.reindex(columns=sorted(df_pivot.columns, key=convert_str_to_int))

# return df_pivot

#mongodb에 저장된 입력한 년도중 하반기 데이터 가져오기
# @app.get('/month_firemongo')
# async def month_firemongo(year=None):
#     if year is None:
#         return "'년도(ex,2018)의 입력을 확인해주세요"
#     else:
#         months=["06","07","08","09","10","11","12"]
#         result=await firemongo()
#         data = {key:value for key, value in result.items() if key.split('-')[0] == year and key.split('-')[1] in months}
        
#         #dataframe을 만들고 그걸로 plot를 만들기
#         df = pd.DataFrame({"dataDate": list(data.keys()), "count": list(data.values())})
#         df.set_index("dataDate", inplace=True)
#         df.sort_index(inplace=True)

#          #df['count'] 열의 데이터가 문자열로 되어있어서 그래프를 그리기 안됨
#         df['count']=df['count'].astype(int)

#         df.plot(kind='line', marker='o', figsize=(20, 12),color='red')

#         plt.xlabel("년도-월")
#         plt.ylabel("산불 발생 수")
#         plt.title(f"{year}의 월별 산불 발생 수")

#         #enumerate를 이용해서 for문으로 index와 값을 반환시켜줌
#         for idx, value in enumerate(df['count']):
#             plt.text(x=idx, y=value + 1, s=f"{value}건", horizontalalignment='center')

#         plt.grid(True)
#         plt.savefig(f"seasonfire_month_{year}.png", dpi=400, bbox_inches='tight')

#         # plt.show()

#         return data,f"seasonfire_month_{year}.png saved.."