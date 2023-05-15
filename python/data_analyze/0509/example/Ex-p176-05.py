import numpy as np
from pandas import Series, DataFrame

index = ['봉길','유신','임당']
list1 = [30,40,50]

series = Series(data=list1, index=index)
print('\n시리즈 출력 결과')
print(series)

index=['봉길','유신','순신']
columns=['용산','마포','서대문']
list1 = list(3 * onedata for onedata in range(1,10))

frame = DataFrame(np.reshape(np.array(list1), (3,3)),index=index, columns=columns)
print('\n데이터 프레임 출력 결과')
print(frame)

print('\nDataFrame + Series')
result = frame.add(series, axis=0)
print(result)

index2=['봉길','유신','완용']
columns2=['용산','마포','은평']
list2=list(5* onedata for onedata in range(1,10))

frame2=DataFrame(np.reshape(np.array(list2),(3,3)),index=index2,columns=columns2)
print('\n데이터 프레인 출력 결과')
print(frame2)

print('\ndataframe + dataframe')
r=frame.add(frame2, fill_value=20)
print(r)

print('\ndataframe - dataframe')
r=frame.add(frame2, fill_value=10)
print(r)

