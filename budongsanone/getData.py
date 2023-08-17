
import requests
import json
import pandas as pd
import os
from datetime import datetime

base_dir = "data"
file_nm = "data-"+datetime.now().strftime('%Y-%m-%d-%H-%M-%S')+".xlsx"
xlxs_dir = os.path.join(base_dir, file_nm) 

def apt_type(a):
    if a == '0': return "종합"
    if a == '1': return "아파트"
    if a == '3': return "연립/다세대"
    if a == '7': return "단독"
    return "?"

def price_type(a):
    if a == 'S': return "매매"
    if a == 'D': return "전세"
    if a == 'R': return "월세"
    return "?"

api_url = 'https://api.odcloud.kr/api/HousePriceTrendSvc/v1/getHousePrice'

key = 'ATvxiuQAY0ACpA1oLNO3Xyi8eXSZuiVs6AAt7tPOpyj4dJ+PGJFf4HwJdLKU0UfsQGqzwFOs07sUg09WZtkHwQ=='

headerDict = {}
headerDict.setdefault('Authorization', key)

paramDict = {}
paramDict.setdefault('serviceKey', key)
paramDict.setdefault('page', '1')
paramDict.setdefault('perPage', '1000')
paramDict.setdefault('cond[REGION_CD::EQ]', '26000') # 지역코드 (엑셀 확인)
# paramDict.setdefault('cond[RESEARCH_DATE::LT]', '203012') # 6자리, 조사일자 < YYYYMM
# paramDict.setdefault('cond[RESEARCH_DATE::LTE]', '203012') # 6자리, 조사일자 <= YYYYMM
# paramDict.setdefault('cond[RESEARCH_DATE::GT]', '201001') # 6자리, 조사일자 > YYYYMM
# paramDict.setdefault('cond[RESEARCH_DATE::GTE]', '201001') # 6자리, 조사일자 >= YYYYMM
# paramDict.setdefault('cond[APT_TYPE::EQ]', '0') # 주택유형구분 (0: 종합, 1: 아파트, 3: 연립/다세대, 7: 단독)
# paramDict.setdefault('cond[TR_GBN::EQ]', 'S') # 매매전세월세구분 (S: 매매, D: 전세, R: 월세)
paramDict.setdefault('cond[PRICE_GBN::EQ]', 'A') # 가격구분 (A: 평균가격, AU: 평균단위가격, M: 중위가격, MU: 중위단위가격, AD: 평균월세보증금, AR: 평균월세가격, MD: 중위월세보증금, MR: 중위월세가격)


requestData = requests.get(api_url, params=paramDict, headers=headerDict)

if requestData.status_code != 200:
    print(requestData.status_code, 'Request Bad')
    
else:
    print(requestData.status_code, 'Request OK')
    jsonData = requestData.json()
    parsedata = jsonData['data']
    result1 = json.dumps(parsedata) # str
    result = json.loads(result1) # list
    for data in result:
        print("지역: {}\n주택 유형: {}\n가격: {}\n가격 유형: {}\n조사일자: {}\n".format(data['REGION_NM'],apt_type(data['APT_TYPE']),data['PRICE'],price_type(data['TR_GBN']),data['RESEARCH_DATE']))

    #%%
    df = pd.DataFrame(result)
    df.style
    df.to_excel(xlxs_dir)

