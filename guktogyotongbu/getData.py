
import requests
import xml.etree.ElementTree as et
import pandas as pd
import os
from datetime import datetime
import addressFinder as address



api_url =  'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade'

key = requests.utils.unquote('ATvxiuQAY0ACpA1oLNO3Xyi8eXSZuiVs6AAt7tPOpyj4dJ+PGJFf4HwJdLKU0UfsQGqzwFOs07sUg09WZtkHwQ==')



columList = ['아파트','거래금액','평','면적','층','법정동','년','월','지번','해제여부']
columList2 = ['월','평균거래금액']

headerDict = {}
headerDict.setdefault('Authorization', key)

def getDataFromAPI(region = 11000, ymd = 201512):
    # print("getDataFromAPI")
    paramDict = {}
    paramDict.setdefault('serviceKey', key)
    paramDict.setdefault('LAWD_CD', str(region)) # 지역코드...
    paramDict.setdefault('DEAL_YMD', str(ymd)) # 계약년월(6자리)
    return requests.get(api_url, params=paramDict, headers=headerDict)


def findApartFromData(region, ymd, Dong, Jibun):
    # print("findApt")
    requestData = getDataFromAPI(region, ymd)
    # print("getDataFromAPI success")
    tree = et.fromstring(requestData.content)
    et.indent(tree)
    # print(tree)
    items = tree[1][0]

    listOfItems = []
    valueList = []
    for item in items:
        if Dong == '' or item.find('법정동').text.strip() == Dong:
            if Jibun == '' or item.find('지번').text.strip() == Jibun:
                valueList.append(item.find('아파트').text)
                valueList.append(item.find('거래금액').text.strip())
                valueList.append(str(round(float(item.find('전용면적').text) * 0.3025)))
                valueList.append(item.find('전용면적').text)
                valueList.append(item.find('층').text)
                valueList.append(item.find('법정동').text.strip())
                valueList.append(item.find('년').text)
                valueList.append(item.find('월').text)
                valueList.append(item.find('지번').text)
                valueList.append(item.find('해제여부').text)
                listOfItems.append(valueList)
                valueList = []
    return listOfItems



def getDataInGap(region, start, end, Dong = '', Jibun = ''):
    # print("getDataInGap")
    listOfItems = []
    for ymd in range(start, end+1):
        if ymd%100 <= 12 and ymd%100 > 0:
            print(ymd)
            value = findApartFromData(region, ymd, Dong, Jibun)
            # print("FindApt success")
            listOfItems.append(value)
    return listOfItems


def getData(sd = '부산시', sgg = '동래구', umd = '', jibun = '', day1 = 202201, day2 = 202212):
    max_price = 0
    min_price = 99999
    max_Apt = ''
    min_Apt = ''
    avg_price = 0
    month_avg = 0
    scale_avg = []
    print(["start: ",day1,"end: ",day2])
    print("try getDataInGap")
    result = getDataInGap(address.local(sd, sgg), Dong = umd, Jibun=jibun, start=day1, end=day2)
    dataResult = []
    graphData = []
    for item in result:
        for i in item:
            price = int(i[1].replace(',',''))
            if price > max_price:
                max_price = price
                max_Apt = i[5] + ', ' + i[0] + ', ' + i[2] + '평'
            if price < min_price:
                min_price = price
                min_Apt = i[5] + ', ' + i[0] + ', ' + i[2] + '평'
            avg_price += price
            month_avg += price
            dataResult.append(i)
        graphData.append([item[0][-4][2:]+'.'+item[0][-3], month_avg/len(item)])
        month_avg = 0
    avg_price /= len(dataResult)
    print(['최고가', max_Apt, str(max_price)+'만원', '최저가', min_Apt, str(min_price)+'만원', '평균가', avg_price])
    print("getDataInGap success")
    df = pd.DataFrame(dataResult, columns=columList)
    graphdf = pd.DataFrame(graphData, columns=columList2)
    print("DataFrame success")
    return df, graphdf

def makeExcel(dataFrame, filename = 'data'):
    base_dir = "data"
    file_nm = filename+"-"+datetime.now().strftime('%Y-%m-%d-%H-%M-%S')+".xlsx"
    xlxs_dir = os.path.join(base_dir, file_nm) 
    dataFrame.to_excel(xlxs_dir)
    print("Excel success")

def getDatabyMonth(sd = '부산시', sgg = '동래구', umd = '', jibun = '', day = 202201, month = 12):
    num = month - 1
    if num >= 12:
        y = num / 12
        num %= 12
        num += y*100
    num += day
    return getData(sd=sd, sgg=sgg, umd=umd, jibun=jibun, day1=day, day2=num)

def getDatabyOnlyMonth(sd = '부산시', sgg = '동래구', umd = '', jibun = '', month = 12):
    day = int(datetime.now().strftime('%Y%m'))
    daya = day
    num = month-1
    if num >= 12:
        y = int(num / 12)
        num %= 12
        num += y*100
    if num%100 > daya%100:
        daya -= 100
        daya += 12
    st = daya - num
    if st%100 == 0:
        st -= 100
        st += 12
    
    # print (st)
    return getData(sd=sd, sgg=sgg, umd=umd, jibun=jibun, day1=st, day2=day)
