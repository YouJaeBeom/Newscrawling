# Newscrawling

Newscrawling은 코로나 관련 뉴스를 수집하는 프레임워크입니다.

네이버에서 코로나와 관련된 전체기간의 모든 뉴스를 수집 할 수 있습니다. 

## 크롤링 항목 

크롤링하는 항목들은 날짜, 뉴스의 제목, 뉴스 내용을 수집합니다. 

크롤링 항목
- 날짜
- 뉴스의 제목
- 뉴스의 내용 

## 저장방법 

저장하는 방법은 파일내에 news.csv 의 형태로 날짜, 뉴스의 제목, 뉴스의 내용 총 3가지의 항목을 저장합니다.

파일 명을 수정하고 싶은 경우 pipelines.py 의 def __init__(self) 에서

<code>
def __init__(self):
        self.myCsv = csv.writer(open('news.csv', 'w',encoding='utf-8-sig',newline=''))
        self.myCsv.writerow(['date', 'News_title','News_text'])
</code>

중  오픈 파일명을 바꾸시면 됩니다.

## 실행방법 

실행하는 방법은 아래와 같습니다.

<code> python singleproces.py </code>
