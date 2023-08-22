
import requests
import xml.etree.ElementTree as et
import pandas as pd
import bs4
import os
from datetime import datetime

base_dir = "data"
file_nm = "data-"+datetime.now().strftime('%Y-%m-%d-%H-%M-%S')+".xlsx"
xlxs_dir = os.path.join(base_dir, file_nm) 
api_url =  'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade'

key = 'ATvxiuQAY0ACpA1oLNO3Xyi8eXSZuiVs6AAt7tPOpyj4dJ%2BPGJFf4HwJdLKU0UfsQGqzwFOs07sUg09WZtkHwQ%3D%3D'

headerDict = {}
headerDict.setdefault('Authorization', key)

def getDataFromAPI(region, ymd):
    paramDict = {}
    paramDict.setdefault('serviceKey', key)
    paramDict.setdefault('LAWD_CD', region) # 지역코드...
    paramDict.setdefault('DEAL_YMD', ymd) # 계약년월(6자리)

    return requests.get(api_url, params=paramDict, headers=headerDict)


def findApartFromData(region, ymd, Dong, Jibun):
    requestData = getDataFromAPI(region, ymd)
    tree = et.fromstring(requestData.content)
    et.indent(tree)
    # print(tree)
    status_code = tree[0]
    if status_code[0] != 00:
        return status_code
    items = tree[1][0]

    columList = ['년','월','일','아파트','거래금액','전용면적','법정동','지번','지역코드']
    listOfItems = []
    valueList = []
    for item in items:
        if item.find('법정동').text.strip() == Dong and item.find('지번').text == Jibun:
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
    return listOfItems




def getDataInGap(region, Dong, Jibun, start, end):
    listOfItems = []
    for ymd in range(start, end+1):
        if ymd%100 == 13:
            ymd += 88
        value = findApartFromData(region, ymd, Dong, Jibun)
        if ymd == start and value[0] != '00':
            print(value[1])
            return
        listOfItems.append(value)
    return listOfItems


def main():
    a

    
    
if __name__ == "__main__":
	main()