from pandas import Series

list = [1,2,3,4]
series=Series(data=list, index=['유신','순신','감찬','해군'])

print('\n data type')
print(type(series))

series.index.name='score'
print('\nindex name of series')
print(series.index.name)

print('\nname of index')
print(series.index)

print('\nvalue of series')
print(series.values)

print('\ninformation of series')
print(series)

print('\nrepeat print')
for idx in series.index:
    print('index :' + idx + ', values : ' + str(series[idx]))
print(series.index)

