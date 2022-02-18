import requests
from bs4 import BeautifulSoup
import re


def check_covid():

    data = []
    url = "http://ncov.mohw.go.kr/"
    res = requests.get(url)
    xml = res.text

    soup = BeautifulSoup(xml, 'html.parser')
    date = soup.find('span', class_='livedate').text

    # datalist에 일일확진,사망 -> 누적확진, 사망 -> 7일간 평균 확진, 사망
    # 정보 저정할 datalist 생성
    # 일일확진자수, 7일간 평균 확진자수
    datalist = soup.select(("div.occur_graph table.ds_table tbody tr td:nth-child(5)"))

    for idx, i in enumerate(datalist, ):
        data.append(datalist[idx].text)

    # 일일사망자수, 7일간 평균 사망자수
    datalist = soup.select(("div.occur_graph table.ds_table tbody tr td:nth-child(2)"))
    for idx, i in enumerate(datalist, ):
        data.append(datalist[idx].text)

    # 누적사망자, 확진자
    datalist = soup.select(("div.occur_num div.box"))
    for idx, i in enumerate(datalist, ):
        #정규표현식으로 숫자만 추출
        matched = re.search(r'([0-9,]+)', datalist[idx].text)
        if matched:
            accumulated = matched.group(1)
        data.append(accumulated)

    return date, data

