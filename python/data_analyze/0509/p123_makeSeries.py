from pandas import Series
import numpy as np

list = [-1,-2,-3]
getout=['짱깨','쪽바리','매국노']

print('\n#cast 1')
myseries = Series(list)
print(myseries)

print('\n#cast 2')
myseries = Series(data=list) #8번과 12번은 같은 거임
print(myseries)

print('\n#cast 3')
myseries = Series(data=list, index=getout)
print(myseries)

print('\n#cast 4')
myseries = Series(data=list, index=getout, dtype=float)
print(myseries)