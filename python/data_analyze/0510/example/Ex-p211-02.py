from pandas import DataFrame as dp
import numpy as np

myindex=['강감찬','김유신','이순신']
mycolumns=['국어', '수학','영어']
mylist=[60.00, np.nan, 90.00, np.nan, 80.00, 50.00, 40.00, 50.00, np.nan]

myframe=dp(np.reshape(mylist,(3,3)), index=myindex, columns=mycolumns)
print(myframe)
print('-'*50)

myframe.loc[myframe['국어'].isnull(), '국어']=myframe['국어'].mean()
myframe.loc[myframe['영어'].isnull(), '영어']=myframe['영어'].mean()
myframe.loc[myframe['수학'].isnull(), '수학']=myframe['수학'].mean()

print(myframe)