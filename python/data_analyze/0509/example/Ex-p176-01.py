from pandas import Series

list=[200,300,400,500]
series = Series(data=list, index=['오공','팔계','오정','법사'])

series.index.name = '실적현황'
print('\n# 시리즈의 색인 이름')
print(series.index.name)

series.name = '직원 실적'
print('\n# 시리즈의 이름')
print(series.name)

print('\n #반복해 출력하기')
for idx in series.index:
    print(' 색인 : '+ idx + ', 값 : '+ str(series[idx]))
