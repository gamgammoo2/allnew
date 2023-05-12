import pandas as pd

filename='data02.csv'
df=pd.read_csv(filename, header=None,  names=['학년','국','영','수'])

df.index.name = '이름'
df.loc[['호민'],['영']]=40
df.loc[['영희'],['국']]=30

print(df)