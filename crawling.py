from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from kiwipiepy import Kiwi
from collections import Counter
from wordcloud import WordCloud 
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from datetime import datetime
import os
import schedule
import time

# 조회할 URL
# 네이버 뉴스 검색어: 개발자, 옵션: 관련도순
url = [
    "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EA%B0%9C%EB%B0%9C%EC%9E%90&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=36&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=1",
    "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EA%B0%9C%EB%B0%9C%EC%9E%90&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=54&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=11"
]

# 워드클라우드 모양 설정
PATH = os.getcwd()
cand_mask=np.array(Image.open(os.path.join(PATH,'image\Cloud.png')))

# 페이지에서 URL 추출하기
def UrlList():
    urlList = []
    for val in url:
        html = urlopen(val)
        bsObject = BeautifulSoup(html, "html.parser")
        for link in bsObject.find_all('a',{'class':'news_tit'}):
            urlList.append(link.get('href'))      
    # print(urlList)      
    return urlList

# 페이지 텍스트 추출하기
def UrlText():
    urlList = UrlList()
    textList = []
    
    for val in urlList:
        try:
            html = urlopen(val)
            bsObject = BeautifulSoup(html, "html.parser")
            for data in bsObject.select('p,div'):
                #줄바꿈, 탭은 공란 처리
                textList.append(re.sub('\n|\t','',data.text.strip()))
        except:
            print("URL Error :", val)
    # print(textList)
    return textList

# 형태소 분석
def VocaList(n):    
    textList =  UrlText()
    # NNG 일반 명사
    # NNP 고유 명사
    # VV  동사
    # VA  형용사
    # XR  어근
    # SL  알파벳(A-Z a-z)
    주요품사 = ['NNG', 'NNP', 'VV', 'VA', 'XR', 'SL']
    용언품사 = ['VV', 'VA']
    counter = Counter()
    kiwi = Kiwi()
    dictionary = {}
    for val in textList:
        try:            
            result = kiwi.tokenize(val)
            for token in result:
                if token.tag in 주요품사:
                    counter.update([(token.form,token.tag)])                      
        except:
            print("Change Error",val)
    
    for(형태소, 품사), 개수 in counter.most_common(n):
        if 품사 in 용언품사:
            형태소 += "다"
        # print(f"{형태소},{개수}")
        dictionary[형태소] = 개수
    
    wordcloud = WordCloud(
        font_path = 'malgun.ttf', # 한글 글씨체 설정
        background_color='white', # 배경색은 흰색으로 
        colormap='Blues', # 글씨색은 빨간색으로
        mask=cand_mask, # 워드클라우드 모양 설정
    ).generate_from_frequencies(dictionary)
    
    # 파일이름 설정
    now = datetime.now()    
    file_name = "cloud\word_cloud_" + now.strftime("%Y-%m-%d");
      
    #사이즈 설정 및 출력
    plt.figure(figsize=(10,10))
    plt.imshow(wordcloud,interpolation='bilinear')
    plt.axis('off') # 차트로 나오지 않게
    plt.savefig(os.path.join(PATH,file_name)  )
    print(file_name,' 생성 완료')

# 매 시간 실행
schedule.every().hour.do(VocaList,n=100)

while True:
    schedule.run_pending()
    time.sleep(1)
    