# <한국공항공사 항공(공항) 산업 발전 전략 공모전>

- 박다현, 이성우


## 기사를 통해 알아보는 COVID-19이 항공사의 미친 영향


### 기간
    1) 2019년 07월 ~ 2019년 11월 (COVID-19 발생 전)
    2) 2019년 12월 ~ 2020년 04월 (COVID-19 발생)
    3) 2020년 05월 ~ 2020년 10월 (경제가 조금 회복되는 시기) -> 논문근거자료 찾는 중


- 2), 3) 기간 기사 크롤링 완료


### 연구방법

- 우선 네이버 뉴스를 통해 크롤링 진행
- 네이버 뉴스 포맷을 제공하는 기사만 크롤링
- 네이버 뉴스는 하나의 기간 검색에 최대 4000건의 기사만을 제공
- 따라서 기간을 잘게 나눌수록 유리함
- 일주일 간격으로 기간을 나누었음 (아래 예시)
- 
    ```python
    day_start = ["2019.12.01", "2019.12.08", "2019.12.15", .....
    day_end = ["2019.12.07", "2019.12.14", "2019.12.21", .....
    ]
    ```

- 간격을 일주일로 수정하면 대부분의 기간에서 기사수가 4000개를 넘지 않음
    ```
    ...
2020.06.21 오류 발생, 제공 기사수 4000개 이하
url 수집 완료(1483개), 기사 추출 시작
naver_article/article_list_2020.06.21_2020.06.27: 완료
기사 개수: 1468
2020.06.28 오류 발생, 제공 기사수 4000개 이하
url 수집 완료(1344개), 기사 추출 시작
naver_article/article_list_2020.06.28_2020.07.04: 완료
기사 개수: 1342
2020.07.05 오류 발생, 제공 기사수 4000개 이하
url 수집 완료(1261개), 기사 추출 시작
naver_article/article_list_2020.07.05_2020.07.11: 완료
기사 개수: 1257
2020.07.12 오류 발생, 제공 기사수 4000개 이하
url 수집 완료(1558개), 기사 추출 시작
naver_article/article_list_2020.07.12_2020.07.18: 완료
기사 개수: 1546
2020.07.19 오류 발생, 제공 기사수 4000개 이하
url 수집 완료(1372개), 기사 추출 시작
naver_article/article_list_2020.07.19_2020.07.25: 완료
기사 개수: 1371
2020.07.26 오류 발생, 제공 기사수 4000개 이하
url 수집 완료(1158개), 기사 추출 시작
naver_article/article_list_2020.07.26_2020.08.01: 완료
기사 개수: 1152
    ```
- 위의 예시는 해당 기간의 4000개의 기사 중 몇개의 기사를 크롤링 했는지를 나타냄

### 전처리

- 수집한 기사의 본문에서 다음과 같은 문자열을 삭제해주었음
    1. "// flash 오류를 우회하기 위한 함수 추가 function _flash_removeCallback() {}" 
    2. "동영상 뉴스"
    3. []로 감싸진 문장 `(\[[^)]*\])` 이거 어케하는지 모르겠다 젠장...
    4. 특수문자

- 다음과 같이 시기를 묶어주었음
  - 1) 2019년 07월 ~ 2019년 11월 (COVID-19 발생 전)
    1) 2019년 12월 ~ 2020년 04월 (COVID-19 발생)
    2) 2020년 05월 ~ 2020년 10월 (경제가 조금 회복되는 시기) 

    ```python
    article_1912_2004.to_csv('naver_article/article_1912_2004.csv', encoding='utf-8-sig', index=False)
    ```
    ~~처음에 기사 모을때도 index=False 옵션 넣을껄...~~

  - article_1912_2004는 22445rows
  - article_2004_2010는 24393rows


### 0903 수정사항
1. 기간수정
   1. 19.06 ~ 19.11
   2. 19.12 ~ 20.05
   3. 20.06 ~ 20.11
   <br>
2. 검색 키워드 수정
   1. 코로나, 항공 -> 항공사
   <br>
3. 검색 단위기간 수정
   - 일주일 단위 검색 -> 하루 단위 검색 후 일주일 단위로 저장