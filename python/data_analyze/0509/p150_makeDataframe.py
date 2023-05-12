from pandas import DataFrame as dp
import numpy as np

mydata = np.arange(9).reshape((3,3))
myframe=dp(data=mydata, index=['용산','마포','은평'],columns=['대만','대협','우성'])
print(myframe)
print('-'*50)

sdata = {'지역' : ['용산','마포'],'연도' : [2019,2020]}
myframe = dp(data=sdata)
print(myframe)
print('-'*50)

sdata = {'용산' : {2020:10,2021:20},'마포': {2020:30,2021:40,2022:50}}
myframe = dp(data=sdata)
print(myframe)
print('-'*50)

sdata = {'지역' : ['용산','마포','용산','마포','마포'],'연도' : [2019,2020,2021,2020,2021], '실적' : [20,30,35,25,45]}
myframe = dp(data=sdata)
print(myframe)
print('-'*50)


