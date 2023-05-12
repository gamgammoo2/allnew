from pandas import DataFrame

sdata = {
    '도시': ['서울','서울','서울','부산','부산'],
    '연도': [2000,2001,2002,2001,2002],
    '실적': [150,170,360,240,290]
}

myindex = ['one','two','three','four','five']
myframe = DataFrame(sdata, index=myindex)
print('\n type :', type(myframe))

myframe.columns.name = 'columns1'
print('\n index information')
print(myframe.columns)

myframe.index.name = 'index1'
print('\n index information')
print(myframe.index)

print('\n inner data information')
print(type(myframe.values))
print(myframe.values)

print('\n data type information')
print(myframe.dtypes)

print('\n context information')
print(myframe)

print('\n row, col transform')
print(myframe.T)

print('\n col property usage')
mycolumns = ['연도','도시','실적']
newframe=DataFrame(sdata, columns=mycolumns)
print(newframe)



