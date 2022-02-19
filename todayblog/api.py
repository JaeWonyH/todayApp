from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
import re

#오늘의 날씨 웹 스크래핑
def check_weather():
    data = []
    url = 'https://search.naver.com/search.naver?query=날씨'
    res = requests.get(url)
    xml = res.text
    soup = BeautifulSoup(xml, 'html.parser')

    data1 = soup.find('div', {'class': '_tab_flicking'})
    #현재 위치 정보
    address = data1.find('h2', {'class':'title'}).text
    data.append(address)
    #현재 온도
    data2 = data1.find('div',{'class':'temperature_text'})
    temp = data2.find('strong').text
    matched = re.search(r'([0-9]+)', temp)
    #현재 온도에서 숫자만 뽑음
    tmp = matched.group(1)
    data.append(tmp)
    #summary: 어제와의 기온 비교 및 기상 요약
    data3 = data1.find('div',{'class':'temperature_info'})
    summary = data3.find('p',{'class':'summary'}).text
    data.append(summary)
    #강수확률 , 습도 ,바람(서풍)
    data4 = data1.find('dl',{'class':'summary_list'})
    rain_rate = data4.find_all('dd',{'class':'desc'})[0].text
    moisture = data4.find_all('dd',{'class':'desc'})[1].text
    wind = data4.find_all('dd',{'class':'desc'})[2].text
    data.append(rain_rate)
    data.append(moisture)
    data.append(wind)
    #오늘의 미세먼지, 초미세먼지, 자외선,일출/일몰
    data5 = data1.find('div',{'class':'report_card_wrap'})
    dust = (data5.find_all('li',{'class':'item_today level1'})[0]).find('span').text
    mini_dust = (data5.find_all('li',{'class':'item_today level1'})[1]).find('span').text
    radio = (data5.find_all('li',{'class':'item_today level1'})[2]).find('span').text
    sun_type = (data5.find('li',{'class':'item_today type_sun'})).find('strong').text
    sun_time = (data5.find('li',{'class':'item_today type_sun'})).find('span').text
    data.append(dust)
    data.append(mini_dust)
    data.append(radio)
    data.append(sun_type)
    data.append(sun_time)
    # 현재 위치, 현재 온도, 어제와의 기온비교 및 기상요약, 강수확률, 습도, 바람, 미세먼지,초미세먼지, 자외선, 일출/일몰,시간
    return data



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

