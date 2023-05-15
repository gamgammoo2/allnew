from pandas import Series

index1=['춘향','몽룡','봉사']
list1=[40,50,60]

index2=['춘향','몽룡','어멈']
list2=[20,40,70]

series1=Series(data=list1, index=index1)
series2=Series(data=list2, index=index2)

print('\n # 시리즈 1')
print(series1)

print('\n # 시리즈 2')
print(series2)

print('\n # 두시즈 덧셈')
seriesadd=series1.add(series2, fill_value=10)
print(seriesadd)

print('\n # 두시즈 뺄셈')
seriessub=series1.sub(series2, fill_value=30)
print(seriesadd)

