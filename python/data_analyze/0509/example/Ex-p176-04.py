from pandas import DataFrame

sdata = {
    '국' : [40,60,80,50,30],
    '영': [55,65,75,85,60],
    '수': [30,40,50,60,70]
}

index = ['감찬','순신','유신','구','중근']
frame=DataFrame(sdata, index=index)
print(frame)

print('\n #짝수행 읽어보소')
r=frame.iloc[0::2]
print(r)

print('\n #이순신 행만 시리즈로 읽어보소')
r=frame.loc['순신']
print(r)

print('\n #강감찬 영어점수 읽어보소')
r=frame.loc[['감찬'],['영']]
print(r)

print('\n #중근, 감찬의 국/수 점수 읽어보소')
r=frame.loc[['중근','감찬'],['국','수']]
print(r)

print('\n #순신,김구 영어 점수 80으로 ')
frame.loc[['순신','구'],['영']] = 80
print(r)

print('\n # 순신~구 수학 점수 100으로')
frame.loc['순신':'구',['수']]=100
print(r)
