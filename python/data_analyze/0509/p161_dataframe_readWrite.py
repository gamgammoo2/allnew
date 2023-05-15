import numpy as np
from pandas import DataFrame

myindex = ['이순신','김유신','강감찬','광해군','연산군']
mycolumns=['서울','부산','광주','목포','경주']
mylist=list(10*onedata for onedata in range(1,26))
print(mylist)

myframe = DataFrame(np.reshape(mylist,(5,5)),index=myindex, columns=mycolumns)
print(myframe)

print('\n1 row data read of series')
result = myframe.iloc[1]
print(type(result))
print(result)

print('\nmulti row data read of series')
result = myframe.iloc[[1,3]]
print(type(result))
print(result)

print('\even row data read of series')
result = myframe.iloc[0::2]
print(type(result))
print(result)

print('\nodd data read of series')
result = myframe.iloc[1::2]
print(type(result))
print(result)

print('\n김유신 included row data read of series') #인덱스로 읽을 때는 아이록. 데이터를 가져오고 싶으면 록
result = myframe.loc['김유신']
print(type(result))
print(result)

print('\n김유신 included row data read of dataframe')
result = myframe.loc[['김유신']]
print(type(result))
print(result)

print('\n이순신,강감찬 included row data read of dataframe')
result = myframe.loc[['이순신','강감찬']]
print(type(result))
print(result)

print(myframe.index)
print('-'*50)

print('\nin 이순신 row, 광주 실적 included row data read of dataframe')
result = myframe.loc[['이순신'],['광주']]
print(type(result))
print(result)

print('\n연산군, 강감찬/광주,목포실적 included row data read of dataframe')
result = myframe.loc[['연산군', '강감찬'],['광주','목포']]
print(type(result))
print(result)

print('\n이순신~강감찬/서울~목포 실적 included row data read of dataframe')
result = myframe.loc['이순신':'강감찬','서울':'목포']
print(type(result))
print(result)

print('\n김유신~광해군/부산 실작 included row data read of dataframe')
result = myframe.loc['김유신' : '광해군',['부산']]
print(type(result))
print(result)

print('\n boolean data process')
result = myframe.loc[[False, True, True, False, True]]#보고싶은 것만 true
print(result)

print('\n부산 실적 <= 100')
result = myframe.loc[myframe['부산'] <=100]
print(result)

print('\n목포 실적 == 140')
result = myframe.loc[myframe['목포'] ==140]
print(result)

cond1 = myframe['부산']>=70 #집중도
cond2 = myframe['목포']>=140

print(type(cond1))
print('-'*50)

df = DataFrame([cond1, cond2])
print(df)
print('-'*50)

print(df.all())
print('-'*50)


print(df.any()) #김유신도 포함됨
print('-'*50)

result = myframe.loc[df.all()]
print(result)
print('-'*50)

print('\n lambda function')
result = myframe.loc[lambda df : df['광주'] >= 130]
print(result)

print('\n data set 30 => 이순신, 강감찬 부산 실적')
myframe.loc[['이순신','강감찬'],['부산']] =30
print(myframe)

print('\n data set 30  over => 이순신 어디지역 실적') #True False로 나옴
result=myframe.loc[['이순신']] >=30
print(result)

print('\n data set 80 => 김유진 ~광해군 경주 실적')
myframe.loc['김유신':'광해군','경주'] =80
print(myframe)


print('\n data set 50 => 연산군 모든 실적') #연산군 행이라서 대괄호 두개, 모든이라서 : 을 사용
myframe.loc[['연산군'],:] =50
print(myframe)


print('\n data set 60 => 모든 사람 광주 실적')
myframe.loc[:,['광주']] =60
print(myframe)
print('-'*50)

print('\n data set 0=> 경주 실적<= 60 이하인 사람의 경주, 광주 실적')
myframe.loc[myframe['경주'] <= 60, ['경주','광주']] =0
print(myframe)

