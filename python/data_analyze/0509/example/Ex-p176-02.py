from pandas import Series

index=['감찬','순신','유신','해군','산군','문덕']
list = [5,6,4,8,7,2]
series = Series(data=list, index=index)
print(series)

print('\n 1번째 항목 100점으로')
series[1]=100
print('\n 2~4번째 항목 99점으로')
series[2:4]=99
print('\n 감찬, 문덕을 30점으로')
series[['감찬','문덕']]=30

print('\n 시리즈 내용 확인')
print(series)
