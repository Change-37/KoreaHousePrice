import requests
import xml.etree.ElementTree as et

api_url = "https://business.juso.go.kr/addrlink/addrLinkApi.do"
search_key = requests.utils.unquote("devU01TX0FVVEgyMDIzMDgyMjA5MzU0MTExNDAzODA=")
# popup_key = "devU01TX0FVVEgyMDIzMDgyMjEyMTE1OTExNDAzOTE="


def local(sido, gungu):
    paramDict = {}
    paramDict.setdefault('confmKey', search_key)
    paramDict.setdefault('keyword', sido+gungu) # '서울시송파구'
    requestData = requests.get(api_url, params=paramDict)

    tree = et.fromstring(requestData.content)
    et.indent(tree)
    items = tree[1]
    sggCode = items.find('admCd').text[:5]
    return sggCode


local('서울시', '송파구')