import pandas as pd

filename= 'seoul.csv'
df=pd.read_csv(filename)
print(df)

# result=df.loc['강남구 신사동']->내가 만든 오류
#강남구 신사동이고 단지명이 삼지인 데이터에 해당하는 것만 뽑아오기
result=df.loc[(df['시군구']==' 서울특별시 강남구 신사동') & (df['단지명']=="삼지")]
print('\n ---------------신사동 데이터 --------------------------------')
print(result)

#도로명을 인덱스로
newdf = df.set_index(keys=['도로명'])
print(newdf)

# result=newdf.loc[(newdf['도로명']=='언주로')]
##인덱스가 도로명이라서,인덱스가 lable이라서 디멘젼 형태로 찾음
result=newdf.loc[['언주로']]
print(result)

result=newdf.loc[['동일로']]
print(result)
count=len(newdf.loc['동일로'])
print(count)

