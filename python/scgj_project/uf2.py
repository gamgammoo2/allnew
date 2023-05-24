import json, urllib.request, math
import os.path
from pymongo import mongo_client


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

HOSTNAME = get_secret("ATLAS_Hostname")
USERNAME = get_secret("ATLAS_Username")
PASSWORD = get_secret("ATLAS_Password")

client = mongo_client.MongoClient(f'mongodb+srv://{USERNAME}:{PASSWORD}@{HOSTNAME}')
print('Connected to Mongodb....')

mydb = client['test']
mycol = mydb['projectdb']

def getRequestUrl(url):
    req = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(req)
        # print(response)
        if response.getcode() == 200:
            return response.read().decode('utf-8')
    except Exception as e:
        # print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

def ultrafine(numOfRows,pageNo,year):
    end_point = 'http://apis.data.go.kr/B552584/UlfptcaAlarmInqireSvc/getUlfptcaAlarmInfo'

    parameters = ''
    parameters += "?serviceKey=" + get_secret("data_apiKey")
    parameters += "&returnType=json" 
    parameters += "&numOfRows=" + str(numOfRows) 
    parameters += "&pageNo=" + str(pageNo)  
    parameters += "&year=" +str(year)
    parameters += "&itemCode=PM25"
    url = end_point + parameters


    # print('URL')
    # print(url)

    result = getRequestUrl(url)
    if (result == None):
        return None
    else:
        # dict_type=xmltodict.parse(result)
        # json_type=json.dumps(dict_type)
        # dict2_type=json.loads(json_type)
        # return json_type
        return json.loads(result)

#sn필드를 기준으로 입력되는 년도의 중복되는 데이터를 검색하기
def duplica(sn,year):
    query = {"sn":sn,"dataDate":{"$regex":f"^{year}"}}
    count = mycol.count_documents(query)
    return count > 0

#api로 년도를 입력하면 데이터를 얻어와 mongodb에 넣음(이때, 중복데이터는 안들어가게 처리)
def save_data_to_mongodb(year):
    pageNo = 1
    numOfRows = 100
    nPage = 0  
    dictResult = [] 
    while(True):
        # print('pageNo : %d, nPage : %d, year:%d' % (pageNo, nPage,year))
        dictData = ultrafine(numOfRows,pageNo,year)
        # print('-'*50)
        # print(dictData)

        if (dictData['response']['header']['resultCode'] == "00"):
            totalCount = dictData['response']['body']['totalCount']
            # print('데이터 총 개수 : ', totalCount)  

            for item in dictData['response']['body']['items']:
                if not duplica(item["sn"],year):
                    dictResult.append(item)

            if totalCount == 0:
                break
            nPage = math.ceil(totalCount / numOfRows)
            if (pageNo == nPage):  
                break  

            pageNo += 1
        else :
            break
    if dictResult:
        mycol.insert_many(dictResult)
    return "데이터 추가되었습니다."