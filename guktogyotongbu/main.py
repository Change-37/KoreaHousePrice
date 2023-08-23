import getData
import drawGraph

sido = '부산시' # 검색할 시/도
sigungu = '동래구' # 검색할 시/군/구
upmendong = '' # 검색할 읍/면/동
jibun = '' # 아파트 하나만 검색할 때
start = 202201 # 검색 시작일
end = 202212 # 검색 종료일
month = 20 # 몇 개월로 검색할 시


# dataFrame = getData.getData(sd=sido, sgg=sigungu, umd=upmendong, jibun=jibun, day1=start, day2=end) # 실행시키면 데이터프레임을 받아옵니다.
#dataFrame = getData.getDatabyMonth(sd=sido, sgg=sigungu, umd=upmendong, jibun=jibun, day=start, month=month) # 시작일 ~ n개월 기간
dataFrame = getData.getDatabyOnlyMonth(sd=sido, sgg=sigungu, umd=upmendong, jibun=jibun, month=month) # 시작일 ~ n개월 기간

getData.makeExcel(dataFrame) # 받아온 데이터프레임 엑셀파일로 저장
