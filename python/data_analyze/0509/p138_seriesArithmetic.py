from pandas import Series, DataFrame

myindex1=['백호','태웅','대협','대만']
mylist1=[70,80,90,100]

myindex2=['백호','태웅','치수','태섭']
mylist2=[100,90,80,70]

myseries1=Series(data=mylist1, index=myindex1)
myseries2=Series(data=mylist2, index=myindex2)

print('\n# data of series1')
print(myseries1)

print('\n# data of series2')
print(myseries2)

#arithmetic
print(myseries1 + 5)
print('-'*50)

print(myseries1.add(5))
print('-'*50)

print(myseries1 -10)
print('-'*50)

print(myseries1 *2)
print('-'*50)

print(myseries1 /3)
print('-'*50)

#relation operation
print(myseries1>=40)
print('-'*50)

print('\nadd of series(if nodata then NaN)')
newseries=myseries1+myseries2
print(newseries)

print('\nsub of series(operation after fill value 0)')
newseries=myseries1.sub(myseries2,fill_value=0)
print(newseries)
