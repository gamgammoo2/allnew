from bs4 import BeautifulSoup
import numpy as np
from pandas import DataFrame as df
import matplotlib.pyplot as plt

html=open('ex5-10.html','r',encoding="utf-8")
soup=BeautifulSoup(html, 'html.parser')

result =[]
tbody = soup.find("tbody")
tds=tbody.findAll('td')
for data in tds:
    result.append(data.text)
print(result)
print('-'*50)

mycolumns=['이름','국어','영어']
myframe = df(np.reshape(np.array(result),(4,3)),columns=mycolumns)
myframe=myframe.set_index('이름')
print(myframe)
print('-'*50)

plt.rc('font', family='Malgun Gothic')

myframe.astype(float).plot(kind='line', title='Score', legend=1)

filename='score.png'
plt.savefig(filename, dpi=400, bbox_inches='tight')
print(filename + ' Saved....')
plt.show()