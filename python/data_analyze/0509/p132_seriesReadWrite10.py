from pandas import Series

myindex=['용산','마포','영등포','서대문','광진','은평','서초']
mylist=[5,6,4,8,7,3,2]
myseries=Series(data=mylist, index=myindex)
print(myseries)

print('\nread value')
print(myseries[['서대문']])

print('\nslicing label name')
print(myseries['서대문':'은평'])

print('\nslicing label name')
print(myseries['서대문':'은평'])

print('\ndata read')
print(myseries['서대문':'서초'])

print('\nread index')
print(myseries[[2]])

print('\nread index 0,2,4')
print(myseries[0:5:2])

print('\nread index 1,3,5')
print(myseries[[1,3,5]])

print('\nslicing')
print(myseries[3:6])

myseries[2]=9
myseries[2:5]=3
myseries[['용산','서대문']]=5
myseries[0::2]=8
print('\nSeries list')
print(myseries)
