from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
import re

#종목별 뉴스 기사 웹 스크래핑
def check_news(section):
    #제목 , url정보 닮을 datalist
    data=[]

    url_dict = {'정치': 100, '경제': 101, '사회': 102, '생활/문화': 103, '세계': 104, 'IT/과학': 105}
    code = url_dict.get(section)
    url = f'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1={code}'
    req_header_dict ={
            #요청헤더: 브라우저정보
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
    res = requests.get(url, headers=req_header_dict)
    xml = res.text
    soup = BeautifulSoup(xml, 'html.parser')

    atag_list = soup.select(("a[href *='read.naver']"))
    for idx, atag in enumerate(atag_list, 1):
            # <a>뉴스제목</a> -> text, strip()은 공백 제거
        title = atag.text.strip()
        if title:
            # <a>의 href 속성값
            news_link = urljoin(url, atag['href'])
            data.append(title)
            data.append(news_link)

    return data


#코로나 현황 웹 스크래핑
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

