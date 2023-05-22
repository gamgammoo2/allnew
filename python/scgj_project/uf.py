import json, urllib.request, datetime, math
import os.path
import xmltodict

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

def getRequestUrl(url):
    req = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            return response.read().decode('utf-8')
    except Exception as e:
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

def ultrafine():
    end_point = 'https://safemap.go.kr/openApiService/data/getFinedustpm2_5dvsryData.do'

    parameters = ''
    parameters += "?serviceKey=" + get_secret("uf_apiKey")
    parameters += "&numOfRows=" + str(numOfRows) 
    parameters += "&pageNo=" + str(pageNo)  
    parameters += "&dataType=XML"
    url = end_point + parameters
    

    print('URL')
    print(url)

    result = getRequestUrl(url)
    if (result == None):
        return None
    else:
        dict_type=xmltodict.parse(result)
        json_type=json.dumps(dict_type)
        dict2_type=json.loads(json_type)
        return dict2_type
        # return json.loads(result)

dictResult = []

pageNo = 1  
numOfRows = 100 
nPage = 0

while(True):
    print('pageNo : %d, nPage : %d' % (pageNo, nPage))
    dictData = ultrafine()
    print(dictData)

    if (dictData['response']['header']['resultCode'] == "00"):
        totalCount = dictData['response']['body']['totalCount']
        print('데이터 총 개수 : ', totalCount)  

        for item in dictData['response']['body']['items']['item']:
            dictResult.append(item)

        if totalCount == 0:
            break
        nPage = math.ceil(int(totalCount) / numOfRows)
        if (pageNo == nPage):  
            break  

        pageNo += 1
    else :
        break

    savedFilename = 'xx_ultrafine.json'
    with open(savedFilename, 'w', encoding='utf8') as outfile:
        retJson = json.dumps(dictResult, indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(retJson)

    print(savedFilename + ' file saved..')