import pandas as pd

afile = 'android.csv'
bfile = 'iphone.csv'

atable = pd.read_csv(afile, index_col=0, header=0, encoding='utf-8')
btable = pd.read_csv(bfile, index_col=0, header=0, encoding='utf-8')

print(atable)
print('-' * 50)
print(btable)

atable['android'] ='안드로이드'
btable['iphone'] ='아이폰'

print(atable)
print('-' * 50)
print(btable)

mylist = []
mylist.append(atable)
mylist.append(btable)

result = pd.concat(objs=mylist, axis=0, ignore_index=True)

filename = 'result.csv'
result.to_csv(filename, encoding='utf-8')
print(filename + ' Saved...')