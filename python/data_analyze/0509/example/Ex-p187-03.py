import pandas as pd

result =[]
Columns=('이름','나이')
encoding='utf-8'
data=[('철수',10),('영희',20)]

for i in range(0,2):
    이름=data[i][0]
    나이=data[i][1]
    sublist=[]
    sublist.append(이름)
    sublist.append(나이)
    result.append(sublist)

frame = pd.DataFrame(result, columns=Columns)

filename = 'csv_02_01.csv'
frame.to_csv(filename, encoding=encoding, mode='w', index=False)

filename = 'csv_02_02.csv'
frame.to_csv(filename, encoding=encoding, mode='w', index=False, sep='#')

print(filename+'파일 저장 완료')
