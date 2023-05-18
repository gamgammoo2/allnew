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

#list to dict
items_dict = {key : value for key,value in enumerate(items)} #이런 형태를list comprehension이라고함
print(type(items_dict))
print(items_dict)
print('-'*50)

#0의 키값이 생긴걸 벗겨내기->순수한 제이슨이 나옴
items=items_dict[0]
print(type(items))
print(items)
print('-'*50)

df=pd.DataFrame(items,index=[0]).rename(index={0:'result'}).T #인덱스가 0으로 되어있어서 헷갈림. 그래서 바꿈
print(type(df))
print(df)
print('-'*50)

data=df.loc[['gPntCnt','hPntCnt','accExamCnt','statusDt']]
print(type(df))
print(df)
print('-'*50)