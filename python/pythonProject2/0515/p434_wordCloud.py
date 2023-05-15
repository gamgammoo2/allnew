import matplotlib.pyplot as plt
from wordcloud import WordCloud

plt.rcParams['font.family'] = 'Malgun Gothic'

filename = 'steve.txt'
myfile = open(filename, 'rt', encoding='utf-8')

text = myfile.read()

wordcloud = WordCloud()
wordcloud = wordcloud.generate(text)
print(type(wordcloud))
print('-'*50)

frequency=wordcloud.words_
print(type(frequency))
print('-'*50)

sortedData = sorted(frequency.items(), key=lambda x:x[1], reverse=True)
print(sortedData)
print('-'*50)

chartData = sortedData[0:10]
print(chartData)
print('-'*50)

xtick=[]
chart = []
for item in chartData:
    xtick.append(item[0])
    chart.append(item[1])

mycolor=['r', 'g','b','y','m','c','#fff0f0','#ccffbb','#05ccff','#11ccff']
plt.bar(xtick, chart, color=mycolor)
plt.title('top frequency 10')
filename = 'worldCloud1_1.png'
plt.savefig(filename, dpi=400, bbox_inches='tight')
print(filename+'file saved..')

plt.figure(figsize=(20,20))
plt.imshow(wordcloud)
plt.axis('off')

filename = 'worldCloud1_2.png'
plt.savefig(filename, dpi=400, bbox_inches='tight')
print(filename+'file saved..')
