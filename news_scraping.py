import re
import pandas as pd
from bs4 import BeautifulSoup
import requests

# 일주일 간격으로 크롤링
day_start = ["2019.12.01", "2019.12.08", "2019.12.15", "2019.12.22", "2019.12.29", "2020.01.05", "2020.01.12", "2020.01.19", "2020.01.26", "2020.02.02", "2020.02.09", "2020.02.16", "2020.02.23", "2020.03.01", "2020.03.08", "2020.03.15", "2020.03.22", "2020.03.29", "2020.04.05", "2020.04.12", "2020.04.19", "2020.04.26", "2020.05.03", "2020.05.10", "2020.05.17", "2020.05.24", "2020.05.31", "2020.06.07", "2020.06.14", "2020.06.21", "2020.06.28", "2020.07.05", "2020.07.12", "2020.07.19", "2020.07.26", "2020.08.02", "2020.08.09", "2020.08.16", "2020.08.23", "2020.08.30", "2020.09.06", "2020.09.13", "2020.09.20", "2020.09.27", "2020.10.04", "2020.10.11", "2020.10.18", "2020.10.25"]
day_end = ["2019.12.07", "2019.12.14", "2019.12.21", "2019.12.28", "2020.01.04", "2020.01.11", "2020.01.18", "2020.01.25", "2020.02.01", "2020.02.08", "2020.02.15", "2020.02.22", "2020.02.29", "2020.03.07", "2020.03.14", "2020.03.21", "2020.03.28", "2020.04.04", "2020.04.11", "2020.04.18", "2020.04.25", "2020.05.02", "2020.05.09", "2020.05.16", "2020.05.23", "2020.05.30", "2020.06.06", "2020.06.13", "2020.06.20", "2020.06.27", "2020.07.04", "2020.07.11", "2020.07.18", "2020.07.25", "2020.08.01", "2020.08.08", "2020.08.15", "2020.08.22", "2020.08.29", "2020.09.05", "2020.09.12", "2020.09.19", "2020.09.26", "2020.10.03", "2020.10.10", "2020.10.17", "2020.10.24", "2020.10.31"]
headers = {'User-Agent': 'Mozilla/5.0'} 

# 네이버 기사 포맷으로 제공되지만 에러가 발생한 URL
error_url = []

for i in range(len(day_start)):
    covid_news_list = []
    start = day_start[i]
    end = day_end[i]
    for j in range(401): # 기간검색 최대 검색량 4000개 
        try: # 만약 페이지를 넘어가면 오류를 뱉음
            news_url = f'https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EC%BD%94%EB%A1%9C%EB%82%98%2C%20%ED%95%AD%EA%B3%B5&sort=1&photo=0&field=0&pd=3&ds={start}&de={end}&start={j*10+1}'
            req = requests.get(news_url)
            soup = BeautifulSoup(req.text, 'html.parser')

            table = soup.find('ul',{'class' : 'list_news'})
            li_list = table.find_all('li', {'id': re.compile('sp_nws.*')})
            area_list = [li.find('div', {'class' : 'news_area'}) for li in li_list]
            info_list = [info.find('div', {'class' : 'news_info'}) for info in area_list]
            naver_news = [naver.find('a', {'href': re.compile('https://news.naver.com.*')}) for naver in info_list]

            for news in naver_news:
                if news != None:
                    covid_news_list.append(news)
                else:
                    pass
        except: # 오류가 나면 안긴 반복문 종료
            print(f'{start} 오류 발생, 제공 기사수 4000개 이하')
            break
    
    # url을 포함한 a태크 수집
    covid_news_list_url = []

    # a태그에서 href 즉, 기사 url 수집
    for i in covid_news_list:
        covid_news_list_url.append(i.get('href'))

    print(f"url 수집 완료({len(covid_news_list_url)}개), 기사 추출 시작")

    # 뉴스 본문 모으기
    news_list = []
    for url in covid_news_list_url:
        try:
            news_dict = {}
            req = requests.get(url, headers = headers)
            soup = BeautifulSoup(req.text, 'html.parser')

            table = soup.find('div',{'id' : 'main_content'})
            title = table.find('h3', {'id':'articleTitle'})
            body = table.find('div', {'id':'articleBodyContents'})

            # 뉴스 제목과 본문 수집
            news_dict['title'] = title.get_text()
            news_dict['body'] = body.get_text()
            news_list.append(news_dict)
        except:
            # 네이버 기사 포맷으로 제공되지만 에러가 발생한 URL
            print(f'오류 발생, {url}')
            error_url.append(url)
            pass

    article_list = pd.DataFrame(news_list)
    article_list.to_csv(f'naver_article/article_list_{start}_{end}.csv', encoding='utf-8-sig')
    print(f'naver_article/article_list_{start}_{end}: 완료')
    print(f'기사 개수: {len(news_list)}')
