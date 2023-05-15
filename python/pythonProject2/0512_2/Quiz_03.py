import pandas as pd

afile = 'cheogajip.csv'
bfile = 'pelicana.csv'

atable = pd.read_csv(afile, index_col=0, header=0, encoding='utf-8')
btable = pd.read_csv(bfile, index_col=0, header=0, encoding='utf-8')

print(atable)
print('-' * 50)
print(btable)

atable['cheogajip'] ='처갓집'
btable['pelicana'] ='펠리카나'

print(atable)
print('-' * 50)
print(btable)

mylist = []
mylist.append(atable)
mylist.append(btable)

result = pd.concat(objs=mylist, axis=0, ignore_index=True)

filename = 'qz_03.csv'
result.to_csv(filename, encoding='utf-8')
print(filename + ' Saved...')