import os.path
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pandas import DataFrame

keyword = input("검색어를 입력하세요")
response = urlopen("https://search.naver.com/search.naver?where=news&sm=tab_jum&query=" + keyword )
html = response.read()
soup = BeautifulSoup(html, "html.parser")
links = soup.select(".news_tit")
print(links)
# print(links) # 리스트값으로 오기 때문에 for 문으로 풀어줌
for link in links:
    title = link.text
    url = link.attrs['href']
    print(title)
    print(url)