# python으로 워드클라우드 만들기
python으로 키워드로 검색한 뉴스 검색 페이지에서 기사 URL을 추출 후 각 기사를 크롤링하여 워드클라우드를 만드는 프로젝트이다.  

### 1. python 설치  
<a href='https://www.python.org/downloads/'>공식 사이트</a>에서 다운로드 받고 설치한다. 설치 후 cmd 창에서 python -v를 입력 후 버전 정보가 나오면 정상적으로 설치된 것이다.  
<img src="./scan/python site.png"  width="800" >  
  
cmd 창에서 python을 입력하면 python 모드로 진입하여 소스 작성이 가능한데 이는 실제 코딩하는데 한계가 있기에 VS Code를 사용한다.  
<img src="./scan/python cmd.png"  width="800" > 

### 2. VS Code에서 Extension 설치  
Python, Python for VSCode, Python Extension Pack, Python Type Hint 설치  
- Python : 린트, 디버깅, 코드 탐색, 코드 서식 지정, 리팩터링, 변수 탐색기와 같은 기능등을 지원
- Python for VSCode : -> 구문 강조, 스니펫 및 린팅을 지원
- Python Extension Pack : vs code에서 인기많은 extension pack
- Python Type Hint : 입력 모듈 완성 및 type 힌트 자동 완성을 제공  

### 3. py 확장자 파일 생성 및 실행
코드 작성 후 우측 화살표 아이콘을 클릭하면 정상적으로 실행된다.  
<img src="./scan/python test.png"  width="800" >  

그런데 매번 화살표 아이콘을 누르는 작업이 번거로울 뿐더러 장문의 소스를 컨트롤하는데 한계가 있기에 디버깅을 사용한다. Run and Debug를 클릭하면 상단에 선택창이 나오는데 Python File을 클릭하면 된다. 그러면 이후에 F5 버튼으로 디버깅이 가능하다.  
<img src="./scan/python debug.png"  width="800" >  

### 4. 모듈 설치하기  
Python의 경우 pip(Pip Installs Packages)라는 패키지 매니저를 통해 모듈을 다운받고 관리할 수 있다. pip는 Python 다운 시 자동으로 다운되기에 별도로 설치할 필요는 없다. 

pip는 터미널 창에서 `pip install --upgrade` 패키지명 과 같은 방식으로 실행하면 패키지가 설치가 가능하다. 정상적으로 설치되었는지 확인하려면 터미널에서 python 모드로 진입하고 import 모듈을 사용하여 오류가 발생하지 않는지 확인하면 된다. python 모드 종료는 `Ctrl + Z 후 엔터`이다.  
<img src="./scan/python pip.png"  width="800" >  

### 5. 실제 예제 파일 생성하기  
이제 실제로 프로젝트를 저장할 폴더 생성 후 py 확장자 파일을 생성한다.

### 6. 페이지에서 URL 추출하기  
먼저 조회할 페이지의 URL을 배열로 저장한다. 이번 예시에서는 네이버 뉴스를 사용했다.
```python
# 조회할 URL
# 네이버 뉴스 검색어: 개발자, 옵션: 관련도순
url = [
    "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EA%B0%9C%EB%B0%9C%EC%9E%90&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=36&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=1",
    "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EA%B0%9C%EB%B0%9C%EC%9E%90&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=54&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=11"
]
```  
다음으로 해당 URL페이지에 있는 URL(기사링크)을 추출할 것이다.
```python
from urllib.request import urlopen
from bs4 import BeautifulSoup

# 이전 소스

# 페이지에서 URL 추출하기
def UrlList():
    urlList = []
    for val in url:
        html = urlopen(val)
        bsObject = BeautifulSoup(html, "html.parser")
        for link in bsObject.find_all('a',{'class':'news_tit'}):
            urlList.append(link.get('href'))    
    #print(urlList)           
    return urlList
```  
웹 페이지의 정보를 추출하기 위해 beautifulsoup4 모듈을 `pip install requests beautifulsoup4` 명령어로 설치한다.

print 주석을 해제하고 UrlList()를 호출하면 뉴스 검색화면에서 기사 URL들만 추출한 것을 확인할 수 있다. 
<img src="./scan/python UrlList.png"  width="800" >  

참고로 위 예시에서는 네이버 뉴스검색에서 기사 URL의 Class가 news_tit이기에 해당 값으로 필터링한 것이다. 만약 다른 뉴스페이지를 크롤링한다면 개발자도구로 확인 후 class값을 수정해야된다.  

### 7. 페이지 텍스트 추출하기  
뉴스 검색 화면에서 기사 URL을 추출했다면 이제는 각 기사에서 텍스트를 추출할 것이다.  
```python
import re

# 이전소스

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
```  
UrlList를 통해 가져온 URL로 접속하여 텍스트가 들어간 태그에 텍스트만 추출한다. 이때 줄바꿈, 탭의 경우는 정규식으로 공란처리했고 URL 읽기에 실패한 경우 종료되지 않도록 예외처리를 진행했다.  

실제로 실행하면 아래와 같은 결과를 볼 수 있다.
<img src="./scan/python UrlText.png"  width="800" >  

### 8. 형태소 분석하기  
이제 추출한 텍스트의 형태소를 분석하여 각 단어별 빈도를 확인하는 소스를 작성할 것이다.
```python
from kiwipiepy import Kiwi
from collections import Counter

#이전소스

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
```  
형태소 분석을 위해 `pip install kiwipiepy`로 kiwipiepy 모듈을 설치하고 UrlText로 가져온 데이터를 하나씩 형태소 분석하여 빈도수를 카운트한다. 실제 결과값은 아래와 같이 나온다.
<img src="./scan/python VocaList.png"  width="600" >  

### 9. 워드 클라우드 
워드 클라우드란 메타 데이터에서 얻어진 태그들을 분석하여 중요도나 인지도 등을 고려하여 시각적으로 늘어놓아 표시하는 것을 말한다.  
<img src="./scan/word cloud.png"  width="400" >   

이제 추출한 형태소 데이터를 시각화 할 차례이다. wordcloud와 matplotlib 모듈을 사용하여 구름모양의 이미지를 생성할 것이다. 
- wordcloud : `pip install wordcloud`로 설치
- matplotlib : `pip install matplotlib`로 설치

```python
#이전소스
from wordcloud import WordCloud 
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from datetime import datetime
import os

#이전소스

# 워드클라우드 모양 설정
PATH = os.getcwd()
cand_mask=np.array(Image.open(os.path.join(PATH,'image\Cloud.png')))

# 형태소 분석
def VocaList(n):    
    # 이전소스
    
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
```  
먼저 image 폴더를 생성하고 모양을 잡을 이미지를 다운로드 받는다. 그리고 이미지를 저장할 cloud 폴더를 생성한다. 생성 후 위와같이 소스를 작성하고 VocaList를 실행하면 아래와 같이 이미지 파일을 확인할 수 있다.  
<img src="./scan/python wordcloud.png"  width="500" >   

### 10. 스케쥴러 등록하기  
만약 이 작업을 일정 시간 주기로 동작하려면 어떻게 하면 될까? 이때는 schedule 라이브러리를 사용하면 된다. `pip install schedule`로 모듈 설치 후 아래와 같이 소스를 작성한다.  
```python 
import schedule
import time

# 이전소스
schedule.every().hour.do(VocaList,n=100)
# schedule.every(10).seconds.do() 10초마다 실행
# schedule.every(1).minutes.do() 1분마다 실행

while True:
    schedule.run_pending()
    time.sleep(1)
```  
주의할 점은 do()에서 함수명을 기입할 때 전달인자는 콤마로 구분해서 넣어야 된다.

### 11. 응용 프로그램 배포하기  
마지막으로 스케쥴링까지 된 프로그램을 실제 실행파일로 만드는 방법이다. `pip install pyinstaller` 명령어로 pyinstaller 설치 후 CLI 창에서 `pyinstaller py 파일명`을 입력하면 해당 프로젝트 경로(\dist)에 폴더가 생성된다. 실제로 프로그램을 사용할 때는 저 폴더를 복사해서 내부에 .exe 파일을 실행하면 된다.  
<img src="./scan/python exe.png"  width="600" >   