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
mycol = mydb['livetempdb']

def getRequestUrl(url):
    req = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            return response.read().decode('utf-8')
    except Exception as e:
        return None

def livetemp():
    url = 'http://192.168.1.187:5000/temps'

    result = getRequestUrl(url)

    if (result == None):
        return None
    else:
        return json.loads(result)

#월별필드를 기준으로 입력되는 중복되는 데이터를 검색하기
def duplica(mth):
    query = {"기온분석":mth}
    count = mycol.count_documents(query)
    return count > 0

#연결 체크
@app.get('/')
def healthCheck():
    return {"OK":True}

#월별 기온이 mongodb에 저장됨(중복 안되게 처리)
@app.get('/add_livetemp')
async def save_data_livetemp_mongo():
    listResult = []
    listData = livetemp()
    for item in listData:
        if not duplica(item["기온분석"]):
            listResult.append(item)
    
    if listResult:
        mycol.insert_many(listResult)
    # return "데이터 추가되었습니다."
    return {"OK": True, "db": "mongodb", "service": "/add_livetemp"}


from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

#mongodb에 저장된 모든 데이터 가져오기
@app.get('/livetempmongo')
async def livetempmongo():
    result=list(mycol.find({"Unnamed: 1": {"$eq": "전국"}}))#리스트의안의 딕셔너리에서 "Unnamed: 1"키의 값이 "전국"인 것들만 들고와야함
    dict_result={}

    for data in result:
        values = {data["기온분석"]: data["Unnamed: 2"] for key, value in data.items() if key in ["기온분석", "Unnamed: 2"]}
        dict_result.update(values)

    data=dict_result

    df = pd.DataFrame(data.items(), columns=["Key", "Value"])
    
    # "Value" 열 데이터를 숫자형으로 변환
    df["Value"] = df["Value"].astype(float)
    
    # 그래프 생성
    plt.figure(figsize=(15, 9))
    plt.scatter(df["Key"], df["Value"], color="r", label="Data")

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

    # 그래프 출력
    # plt.tight_layout()
    # plt.show()
    plt.savefig(f"livetemp.png", dpi=400, bbox_inches='tight')

    return data,f"livetemp.png saved..."
    # return {"OK": True, "db": "mongodb", "service": "/livetempmongo"}

# --------------------------------------------------------------

def get_secret2(setting, secrets=secrets):
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
mycol = mydb['totaltemp']

def totaltemp():
    url = 'http://192.168.1.187:5001/totaltemp'

    result = getRequestUrl(url)

    if (result == None):
        return None
    else:
        return json.loads(result)
    
#월별필드를 기준으로 입력되는 중복되는 데이터를 검색하기
def duplica2(date):
    query = {"Unnamed: 2":date}
    count = mycol.count_documents(query)
    return count > 0

#연결 체크
@app.get('/')
def healthCheck():
    return {"OK":True}

#월별 기온이 mongodb에 저장됨(중복 안되게 처리)
@app.get('/add_totaltemp')
async def save_data_totaltemp_mongo():
    listResult = []
    listData = totaltemp()
    for item in listData:
        if not duplica2(item["Unnamed: 2"]) and item["Unnamed: 0"] == "0":
            listResult.append(item)
    
    if listResult:
        mycol.insert_many(listResult)
    # return "데이터 추가되었습니다."
    return {"OK": True, "db": "mongodb", "service": "/add_totaltemp"}


#예측
from prophet import Prophet

@app.get('/totaltempmongo')
async def totaltempmongo():
    result = list(mycol.find({"Unnamed: 1": {"$eq": "전국"}}))

    data = []
    for item in result:
        city = item["Unnamed: 1"]
        date = item["Unnamed: 2"]
        meantemp = item["Unnamed: 3"]
        data.append({"ds": date, "y": meantemp})  # Rename columns to "ds" and "y"
    
    df = pd.DataFrame(data)
    df["ds"] = pd.to_datetime(df["ds"])  # Rename "Date" column to "ds"
    df = df.sort_values(by=["ds"], ascending=True)

    plt.figure(figsize=(30, 15))
    plt.plot(df['ds'], df['y'])
    plt.title("2018년부터 전국의 일별 평균 기온")
    plt.xlabel("날짜")
    plt.ylabel("평균 기온")

    # 모델 적합
    model = Prophet(changepoint_prior_scale=3, daily_seasonality=True)
    model.fit(df)  # Fit the model using the modified DataFrame
    
    future = model.make_future_dataframe(periods=120, freq='D')
    forecast = model.predict(future)
    
    #하늘색 : 오차범위 검은점:실제 사용된 데이터
    model.plot(forecast, xlabel='날짜', ylabel='평균 기온')
    
    #prophet은 선색이랑 점색을 바꿀 수 없음
    plt.gca().lines[1].set_color('red')  # 라인 색 바꾸기

    plt.savefig(f"totaltemp9_forecast.png", dpi=400, bbox_inches="tight")

    return "done"

# import seaborn as sns
# # from plotly.offline import init_notebook_mode
# # init_notebook_mode(connected=True)
# import plotly.graph_objs as go

# import os
# plt.style.use('ggplot')

# #마이너스 기호를 인식못해서 하이픈 사용
# #mpl.rcParams['axes.unicode_minus'] = False 이걸 아래에서 적음
# import matplotlib as mpl

# #걔절성 분석
# from statsmodels.tsa.seasonal import seasonal_decompose

# #ACF그래프 그리기
# import statsmodels.api as sm

# #ADF검정으로 정상성 확인
# from statsmodels.tsa.stattools import adfuller

# #mongodb에 저장된 모든 데이터 가져오기
# # @app.get('/totaltempmongo')
# # async def totaltempmongo():
# #     result=list(mycol.find({"Unnamed: 1": {"$eq": "전국"}}))#리스트의안의 딕셔너리에서 "Unnamed: 1"키의 값이 "전국"인 것들만 들고와야함
    
# #     data=[]

# #     for item in result:
# #         city=item["Unnamed: 1"]
# #         date=item["Unnamed: 2"]
# #         meantemp=item["Unnamed: 3"]
# #         data.append({"City":city, "Date":date, "Meantemp":meantemp})
    
# #     df=pd.DataFrame(data)
# #     #date 부분 오름차순 정렬
# #     df["Date"] = pd.to_datetime(df["Date"])
# #     df = df.sort_values(by=["Date"], ascending=True)

# #     df["Meantemp"] = df["Meantemp"].astype(float)

# #     plt.figure(figsize=(30,15))
# #     plt.plot(df['Date'], df['Meantemp'])
# #     plt.title("2018년부터 전국의 일별 평균 기온")
# #     plt.xlabel("날짜")
# #     plt.ylabel("평균 기온")
# #     # plt.savefig(f"totaltemp1_df.png",dpi=400, bbox_inches="tight")

# #     #시계열 형태의 ts 데이터 만들기
# #     timeSeries = df.loc[:,["Date","Meantemp"]]
# #     timeSeries.index=timeSeries.Date
# #     ts=timeSeries.drop("Date",axis=1)

# #     #최신버전은 freq가 아니라 period썼다캄
# #     result = seasonal_decompose(ts['Meantemp'],model='additive',period=365)

# #     fig = plt.figure()
# #     fig=result.plot()
# #     fig.set_size_inches(20,15)

# #     # fig.savefig(f"totaltemp2_ts.png",dpi=400, bbox_inches="tight")
# #     #fig를 보니 데이터들이 패턴을 보임 -> 정상성을 의심
# #     #판단하기 위해 ACF 그래프 그리기 (빠르게 줄어들어야 정상성을 만족한다)
# #     #정상성 : 시계열 데이터의 특성이 시간의 흐름에 따라 변하지 않음을 의미

# #     fig = plt.figure(figsize=(20,8))
# #     ax1 = fig.add_subplot(211)
# #     fig = sm.graphics.tsa.plot_acf(ts, lags=20, ax=ax1)

# #     # fig.savefig(f"totaltemp3_acf.png",dpi=400, bbox_inches="tight")
# #     #서서히 감소 -> 정상성 만족 안함

# #     #단위근 검정인 ADF검정으로 정상성 확인 -> H0(귀무가설): 자료에 단위근 존재. => 정상성 만족 안함. H1(대립가설): 자료가 정상성 만족
# #     #p-value가 0.05(1/2)을 보다 작으면 H0을 기각하므로 정상성을 만족한다.

# #     result = adfuller(ts)

# #     adf = f"ADF Statistic: {result[0]}"
# #     p_value = f"p-value: {result[1]}"
# #     critical = [f"Critical Value: {key}: {value:.3f}" for key, value in result[4].items()]

# #     # 결과를 txt 파일에 저장
# #     with open("totaltemp4_adf.txt", "w") as file:
# #         file.write(adf + "\n")
# #         file.write(p_value + "\n")
# #         for value in critical:
# #             file.write(value + "\n")

# #     #p-value: 0.13525084949444321 >0.05 : 정상성 만족 못함

# #     #1차 차분 시키기(정상성 만족 못하는걸 해결하기 위해서)

# #     ts_diff=ts-ts.shift()
# #     plt.figure(figsize=(22,8))
# #     plt.plot(ts_diff)
# #     plt.title("차분 방법")
# #     plt.xlabel("날짜")
# #     plt.ylabel("평균 온도의 차분")
    
# #     # plt.savefig(f"totaltemp5_diff.png",dpi=400, bbox_inches="tight")

# #     #ADF로 정상성 확인
# #     result = adfuller(ts_diff[1:])
    
# #     adf = f"ADF Statistic: {result[0]}"
# #     p_value = f"p-value: {result[1]}"
# #     critical = [f"Critical Value: {key}: {value:.3f}" for key, value in result[4].items()]

# #     # 결과를 txt 파일에 저장
# #     with open("totaltemp6_adf2.txt", "w") as file:
# #         file.write(adf + "\n")
# #         file.write(p_value + "\n")
# #         for value in critical:
# #             file.write(value + "\n")

# #     #p-value: 1.3266633605169554e-19 <0.05 이므로 정상성 만족

# #     #정상성을 만족하는 차분된 데이터로 ACF와 PACF 그래프를 그려 ARIMA 모형의 p와 q를 결정한다.

# #     fig = plt.figure(figsize=(20,8))
# #     ax1=fig.add_subplot(211)
# #     fig = sm.graphics.tsa.plot_acf(ts_diff[1:], lags=20, ax=ax1)

# #     # fig.savefig(f"totaltemp7_diff_acf.png",dpi=400, bbox_inches="tight")

# #     ax2=fig.add_subplot(212)
# #     fig=sm.graphics.tsa.plot_pacf(ts_diff[1:], lags=20, ax=ax2)

# #     # fig.savefig(f"totaltemp7_diff_pacf.png",dpi=400, bbox_inches="tight")

# #     #ARIMA(2,1,2) : 모델 만들기
# #     from statsmodels.tsa.arima.model import ARIMA

# #     from pandas import to_datetime

# #     # #pdq 최적 구하기
# #     # import itertools
# #     # p=d=q=range(4,7)
# #     # pdq=list(itertools.product(p,d,q))

# #     # # open a file to write the results
# #     # with open('arima_results.txt', 'w') as f:
  
# #     #     # loop over all the parameter combinations
# #     #     for param in pdq:
# #     #         try:
# #     #             model_arima = ARIMA(ts, order=param)
# #     #             model_arima_fit = model_arima.fit()
# #     #             aic = model_arima_fit.aic
                
# #     #             # write the parameter and AIC values to the file
# #     #             f.write(f'{param}: AIC={aic}\n')
                
# #     #         except Exception as e:
# #     #             print(f'Error {e} for param {param}')
# #     #             continue
   
# #     #autoarima -계측값이 일별 m=1, 계절성있으면 seasonal=true
# #     # import pmdarima as pm
# #     # model = pm.auto_arima(ts,seasonal=True, m=1)

# #     #마춤 모델
# #     model = ARIMA(ts, order=(2,1,4))
# #     model_fit = model.fit()

# #     #예측
# #     start_index = pd.to_datetime('2020-01-01')
# #     end_index = pd.to_datetime('2023-09-30')
# #     forecast = model_fit.predict(start=start_index,end=end_index,typ='levels')
   
# #     #시각화
# #     plt.figure(figsize=(22,8))
# #     plt.plot(df.Date,df.Meantemp,label='원본',color='b')
# #     plt.plot(forecast, label='예측', color='r')
# #     plt.title("기온 시계열 예측")
# #     plt.xlabel("날짜")
# #     plt.ylabel("평균 기온")
# #     plt.legend()

# #     plt.savefig(f"totaltemp8_forecast.png",dpi=400, bbox_inches="tight")

# #     return forecast

