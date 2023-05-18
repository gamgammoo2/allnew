import requests
import json
import pandas as pd
from datetime import datetime,timedelta
import os.path

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

url = 'https://apis.data.go.kr/1352000/ODMS_COVID_02/callCovid02Api'#url은 엔드포인트다 (미리보기로 확인)
today = (datetime.today()-timedelta(1)).strftime("%Y%m%d") #년도, 월, 일만 필요해서 .str~을 사용,어제 시간이 필요 timedelte사용 ->위에 선언 필요
print(today)

params = '?serviceKey=' + get_secret("data_apiKey")
params +='&pageNo=1'
params += '&numOfRows=500'
params += '&apiType=JSON'
params +='&status_dt='+str(today)
#여기까지는 필수 데이터

url += params
print(url)

response = requests.get(url) #위에 웹서비스 모듈이 없어 -> 리퀘스트만 써도 원격요청을 할 수 있음 ->데이터는 response의 text에 있다.
print(response)
print('-'*50)

contents = response.text
print(type(contents))
print(contents)
print('-'*50) #json으로 바꿔야함

dict=json.loads(contents)
print(type(dict))
print(dict)
print('-'*50)

items=dict['items'] #제이슨에서 뽑아올때
print(type(items))
print(items)
print('-'*50)

#리스트를 안벗기고 데이터프레임으로 만들기
df = pd.DataFrame(items).rename(index={0:'result'}).T #결과가 붙어서 나와서 전치시키고 싶어서 T를 붙임
print(type(df))
print(df)
print('-'*50)

data=df.loc[['gPntCnt','hPntCnt','accExamCnt','statusDt']]
print(type(data))
print(data)
print('-'*50)

#이제 뽑아왔으니 이걸 몽고디비에 넣거나, 웹에 표시하거나 하는겨
