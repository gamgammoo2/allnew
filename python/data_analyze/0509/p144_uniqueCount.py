from pandas import Series

print('\nunique, count, isin')
mylist=['랄릴락','코슥모슥','코슥모슥','배길홍','코슥모슥','코슥모슥','틀장미','틀장미','랄릴락','랄릴락']
myseries=Series(mylist)

print('\nunique()')
myunique=myseries.unique()
print(myunique)

print('\nvalue_count()')
print(myseries.value_counts())

print('\nisin()')
mask=myseries.isin(['틀장미','랄릴락'])
print(mask)
print('-'*50)

print(myseries[mask])
print('-'*50)

print('\nfinished')