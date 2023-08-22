import requests
import xml.etree.ElementTree as et
import pandas as pd
import bs4

api_url = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade'

key = requests.utils.unquote('ATvxiuQAY0ACpA1oLNO3Xyi8eXSZuiVs6AAt7tPOpyj4dJ+PGJFf4HwJdLKU0UfsQGqzwFOs07sUg09WZtkHwQ==')

headerDict = {}
headerDict.setdefault('Authorization', key)

paramDict = {}
paramDict.setdefault('serviceKey', key)
paramDict.setdefault('LAWD_CD', '26260') # 지역코드...
paramDict.setdefault('DEAL_YMD', '201512') # 계약년월(6자리)

request = requests.get(api_url, params=paramDict, headers=headerDict)

# content = request.text
# xml_obj = bs4.BeautifulSoup(content,'lxml-xml')
# rows = xml_obj.findAll('item')

# for item in rows:
#     print(item)

tree = et.fromstring(request.content)
et.indent(tree)
# print(tree)

items = tree[1][0]

columList = ['년','월','일','아파트','거래금액','전용면적','법정동','지번','지역코드']
listOfItems = []
valueList = []
for item in items:
    if item.find('법정동').text.strip() == '온천동' and item.find('지번').text == '1654':
        valueList.append(item.find('년').text)
        valueList.append(item.find('월').text)
        valueList.append(item.find('일').text)
        valueList.append(item.find('아파트').text)
        valueList.append(item.find('거래금액').text)
        valueList.append(item.find('전용면적').text)
        valueList.append(item.find('법정동').text)
        valueList.append(item.find('지번').text)
        valueList.append(item.find('지역코드').text)
        # for i in item:
        #     if i.tag == '거래금액':
        #         valueList.append(i.text)
        #     if i.tag == '년':
        #         valueList.append(i.text)
        #     if i.tag == '법정동':
        #         valueList.append(i.text)
        #     if i.tag == '아파트':
        #         valueList.append(i.text)
        #     if i.tag == '월':
        #         valueList.append(i.text)
        #     if i.tag == '일':
        #         valueList.append(i.text)
        #     if i.tag == '전용면적':
        #         valueList.append(i.text)
        #     if i.tag == '지번':
        #         valueList.append(i.text)
        #     if i.tag == '지역코드':
        #         valueList.append(i.text)
        listOfItems.append(valueList)
        valueList = []

df = pd.DataFrame(listOfItems)

print(df.head(5))