import numpy as np
import pandas as pd
from pandas import DataFrame, Series

print('\n # 시리즈의 누락 데이터 처리')
print('#원본 시리즈')
myseries = Series(['강감찬','이순신',np.nan,'광해군'])
print(myseries)

print('\n # isnull() 함수 : NaN이면 True')
print(myseries.isnull())

print('\n # notnull() 함수 : NaN이면 True')
print(myseries.notnull())
print('-'*40)

print('\n # notnull() 함수 이용해 참인 항목만 출력')#대괄호를 이용해 묶음
print(myseries[myseries.notnull()])
print('-'*40)

print('\n # dropna() 함수 이용해 누락 데이터 처리') # NaN을 빼는 것
print(myseries.dropna())
print('-'*40)

filename='excel02.csv'
myframe=pd.read_csv(filename, index_col='이름', encoding='utf-8')
print(myframe)

print('\n # dropna() 함수 이용해 누락 데이터 처리') # NaN을 빼는 것
cleaned=myseries.dropna(axis=0)
print(cleaned)
print('-'*40)

print('\n #how="all"이용 누락 데이터 처리')
cleaned=myframe.dropna(axis=0, how='all') #전부 NaN값인 박영희만 제거
print(cleaned)
print('-'*40)

print('\n #how="any"이용 누락 데이터 처리')
cleaned=myframe.dropna(axis=0, how='any')
print(cleaned)
print('-'*40)

print('\n #[영어] 컬럼에 NaN을 제거')
print(myframe.dropna(subset=['영어']))
print('-'*40)

print('\n #컬럼 기준, how="all" 이용 누락 데이터 처리')
cleaned=myframe.dropna(axis=1, how='all')
print(cleaned)
print('-'*40)

print('\n #컬럼 기준, how="any" 이용 누락 데이터 처리')
cleaned=myframe.dropna(axis=1, how='any')
print(cleaned)
print('-'*40)

print('\n ## before : ')
print(myframe)
myframe.loc[['강감찬','홍길동'],['국어']]=np.nan
print('##after : ')
print(myframe)
print('-'*40)

print(myframe.dropna(axis=1, how="all"))

print('## thresh option으로 2를 제거')
print(myframe.dropna(axis=1, thresh=2)) # 암것도 안바뀜 , 뭘 나타냄?  NaN 항목이 두개 "이상" 아닌 항목이 나옴. => 즉 그 축에 입력되어있는 값이 2개 이상이면 나오는 것
print('-'*40)