import requests,json
from bs4 import BeautifulSoup
import pandas
import os.path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
secret_file = os.path.join(BASE_DIR, '../secret.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        errorMsg = "Set the {} environment variable.".format(setting)
        return errorMsg

M = '&numOfRows=1&pageNo=1&stationName=측정소명&dataTerm=DAILY&ver=1.3'
key = get_secret('data_apiKey')
url = 'https://apis.data.go.kr/B552584/ArpltnStatsSvc/getCtprvnMesureSidoLIst?serviceKey='+ key + M

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
ItemList = soup.findAll('item')

for item in ItemList:
    i = item.find('pm25value').text
    s = item.find('pm10grade1h').text
    print('초미세먼지 농도:' + i +'㎍/㎥ ( ' + s + ' )')
    print('( 좋음: 1 ),( 보통: 2 ),( 나쁨: 3 ),( 매우나쁨: 4)')