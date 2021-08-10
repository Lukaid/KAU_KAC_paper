import re
import pandas as pd
from bs4 import BeautifulSoup
import requests

news_url = 'https://search.naver.com/search.naver?where=news&query=%EB%A9%94%EB%A5%B4%EC%8A%A4%2C%ED%95%AD%EA%B3%B5%EC%82%AC&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds=2015.01.01&de=2015.06.15&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Afrom20150101to20150615&is_sug_officeid=0'

req = requests.get(news_url)
soup = BeautifulSoup(req.text, 'html.parser')

news_num = int(input('총 필요한 뉴스기사 수를 입력해주세요(숫자만 입력) : '))  # 가져올 뉴스기사 수 입력

news_list = []
idx = 0
cur_page = 1

print()
print('크롤링 중...')

while idx < news_num:
    # 뉴스 title, link 가져오기
    table = soup.find('ul', {'class': 'list_news'})
    li_list = table.find_all('li', {'id': re.compile('sp_nws.*')})
    area_list = [li.find('div', {'class': 'news_area'}) for li in li_list]
    info_list = [info.find('div', {'class': 'news_info'})
                 for info in area_list]
    naver_news = [naver.find('a', {'href': re.compile(
        'https://news.naver.com.*')}) for naver in info_list]
    # find에서 class로 찾으니 도저히 안나오더라구요,,, 그래서 네이버 기사들은 url이 다 https://news.naver.com 이거로 시작해서
    # 정규표현식을 이용하여 href로 찾아줬습니다.

    for n in naver_news:
        try:  # try는 해당 구문이 에러가 나면 그냥 무시하는 문법입니다. 네이버로 가는 링크가 없으면 오류가 나서 이렇게 해두면 네이버 기사가 없는 기사는 자동으로 거릅니다.
            news_list.append(n.get('href'))
            # 근데 이게 단점이 해당 객체에는 제목이 없어요... 그래서 그냥 dict가 아니라 list로 지정해줬습니다...
            idx += 1
        except:
            pass  # 에러가 난다면(네이버 기사가 없다면) pass

    # 다음 페이지 자동으로 이동, 넥스트 버튼이 다음 페이지의 url정보를 담고 있더라구요...
    pages = soup.find('div', {'class': 'sc_page'})
    next_page_url = pages.find('a', {'class': 'btn_next'}).get('href')

    req = requests.get('https://search.naver.com/search.naver' + next_page_url)
    soup = BeautifulSoup(req.text, 'html.parser')


print('크롤링 완료')

print('데이터프레임 변환')

news_df = pd.DataFrame(news_list)
news_df.to_csv('mers_naver.csv')  # csv로 내보냈습니다.
