+++
title = "Crawling with Python"
description = ""
tags = [
    "crawling",
]
date = "2022-08-30"
categories = [
    "Studylog",
]
menu = "main"
+++

Web crawling recursively finds URLs on a page and repeatedly loads new pages. While a scraper works well when all data is contained within a single page, using a crawler requires careful attention to bandwidth to minimize the load on the target server.

# Quick Techniques

Here are some basic techniques that can scrape and crawl a single domain, single site, and the Internet.

{{% hint info %}}
**Before Building a Crawler**  
For effective crawling, especially for large scale project, check in advance if the data is obtainable through API. Using APIs to retrieve data is generally more efficient in terms of speed: APIs impose less strain on the target server as they provide data in a controlled and optimized manner. 

For example, Wikipedia provides [Wiki API](https://www.mediawiki.org/wiki/API:Main_page).
{{% /hint %}}

## 1. Exploring a Single Domain
<hr>

Let's write a program that crawls HTML text from Wikipedia. Following code crawls a link list from a specifice Wikipedia web page.

```python
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import datetime
import random
import re

# Get different random seed everytime program starts
random.seed(datetime.datetime.now())
def getLinks(articleUrl):
    """
    Inputs:
        articleUrl : Url in 'wiki/...' form
    Outputs:
        List of all URLs in a page of form 'wiki/{articleUrl}' 
    """
    # Get HTML text
    try:
        html = urlopen(f'https://en.wikipedia.org/{articleUrl}')
    except HTTPError as e:
        print(e)
    except URLError as e:
        print('The server could not be found!')
    else:
        print('Got HTML successfully.')

    # Parse HTML text and create bs
    bs = BeautifulSoup(html.read(). 'html.parser')

    # Among tags that contain 'div' and 'id', 
    # return list of URLs that matchs regular expression pattern.
    return bs.find('div', {'id':'bodyContent'}).findAll('a', href=re.compile('^(wiki/)((?!:).)*$'))

# Get search keyword
print('Type keyword to search URL links recursively in wiki.')
target = str(input())

# Get every URL on a page and pick one random URL to print the page.
# Repeat while there are no URLs in the searched page.
links = getLinks('wiki/{target}')
while len(links) > 0: 
    newArticle = links[random.randint(0, len(links)-1)].attrs['href']
    print(newArticle)
    links = getLinks(newArticle)
```


## 2. Crawling the Entire Site
<hr>

### 2.1. 스크랩이 가능한 웹 페이지들
* 표면 웹(Surface Web) : 검색엔진에서 저장하는 부분이다.
* 딥 웹(Deep Web) : 표면 웹의 나머지 부분으로, 인터넷의 90% 정도를 차지한다. 딥웹은 링크되지 않은 페이지나 robots.txt로 차단된 페이지들을 포함하지만, 일부분은 스크랩이 가능하다. 
    - robots.txt 파일은 크롤러 트래픽을 관리하기 위해 사용되며, 사이트에서 접근가능한 URL을 검색엔진 크롤러에 알려준다. 
* 다크 웹(Dark Web) : 딥 웹의 일부분으로, 기존 네트워크 하드웨어 인프라에서 작동하긴 하지만 접근하기 위해 익명 클라이언트 Tor등 특정 프로그램이나 방법을 요구한다. HTTP 위에서 동작하며 보안 채널로 정보를 교환하는 앱 프로토콜을 사용한다. 다크웹을 스크랩하는 데에는 표면 웹을 스크랩하는 것과 다른 방법이 필요하다.
    - Tor(The Onion Router)는 네트워크 우회를 통해 네트워크 익명화를 시행하는 프로그램이다.

### 2.2. 웹사이트 전체 크롤링이 유용한 경우
- 사이트맵 생성 : 크롤러를 통해 사이트 전체를 이동하면서 내부링크를 수집해 페이지들을 폴더구조와 같이 정리할 수 있다. 이를 통해 웹사이트 설계 비용등을 계산할 수 있다.
- 데이터 수집 : 특정 페이지(예를 들어 블로그 포스트나 뉴스 기사 페이지)에 국한해서 검색 플랫폼의 프로토타입을 생성할 때도 재귀적인 크롤링을 이용할 수 있다.

### 2.3. 전체 사이트 크롤링에서 중복 피하기
페이지당 내부 링크가 10개씩 있고 사이트가 다섯 단계로 구성되어있다고 하자. 페이지를 철저히 탐색하기 위해서는 최소 $105$ 페이지에서 $10^5$ 페이지를 탐색해 한다. 그렇지만 실제로 내부 링크 중 중복이 많기 때문에 $10^5$ 페이지를 탐색해야하는 경우는 거의 없다. 

즉 전체 사이트를 크롤링하는 프로그램은 중복 방문을 하지 않는 것이 중요하다. 같은 페이지를 두 번 크롤링하지 않기 위해서는 발견하는 내부 링크를 일정한 형식을 따르도록 해서 집합(Set)에 보관할 수 있다.

```python
# 웹 페이지 중복을 피하기 위해 집합으로 방문한 링크를 관리한다.
pages = set()

def printLinks(pageUrl, recur_cnt):
    """
    위키백과 사이트에서 내부 링크를 100번 재귀 탐색한다. 
    """
    # 재귀 횟수를 100번으로 제한한다.
    recur_cnt += 1
    if recur_cnt > 100: return

    # 프로그램이 동작하는 동안 집합이 유지되도록 한다.
    global pages
    
    # 위키피디아에서 pageUrl을 검색한다.
    try:
        html = urlopen(f'http://en.wikipedia.org/{pageUrl}')
    except HTTPError as e:
        print(e)
    except URLError as e:
        print('The server could not be found!')
    else:
        print('Got HTML successfully.')

    bs = BeautifulSoup(html.read(), 'html.parser')

    # 페이지의 모든 'wiki/...' URL을 탐색하여 출력한다. 
    for link in bs.findAll('a', href=re.compile('^('wiki/')')):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                # 새로운 페이지를 탐색한다.
                newPage = link.attr['href']
                print(newPage)
                pages.add(newPage)
                printLinks(newPage)

# getLinks 함수를 재귀적으로 호출한다.
# Python의 재귀 깊이는 1000회로 제한되어 있으므로, 
# 위키백과 같이 큰 링크 네트워크를 탐색할 때는 재귀 횟수를 제한하도록 한다.
printLinks('', 1)
```

### 2.4. 전체 사이트에서 데이터 수집하기
단순히 URL을 출력하는 것 외에 페이지의 다양한 데이터를 수집해보자.

```python
pages = set()

def printSummary(pageUrl, recur_cnt):
    """
    위키백과 사이트에서 내부링크를 탐색하며 페이지 제목과 첫번째 문단, 편집 링크를 출력한다.
    """
    recur_cnt += 1
    if recur_cnt > 100: return

    global pages
    html = urlopen(f'http://en.wikipedia.org/{pageUrl}')
    bs = BeautifulSoup(html.read(), 'html.parser')

    try: # 다음을 모두 수행하는 경우 항목 페이지이다.
        # 페이지 제목을 출력한다.
        print(bs.h1.get_text())
        # 첫 번째 문단을 출력한다.
        # div#mw-content-text -> p에서 첫번째 문단 태그만 선택한다.
        print(bs.find(id='mw-context-text').findall('p')[0])
        # 편집 링크를 출력한다.
        # li#ca-edit -> span -> a로 탐색한다.
        print(bs.find(id='ca-edit').find('span').find('a').attrs['href'])
    except AttributeError: 
        print('This page is not a content page!')
    
    for link in bs.findAll('a', href=re.compile('^('wiki/')')):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                newPage = link.attrs['href']
                print('-' * 30 + '\n' + newPage)
                pages.add(newPage)
                getLinks(newPage)

printSummary('')
``` 

## 3. Crawling Internet
<hr>

### 3.1. Things to Consider Before Building Web Crawler
- 정해진 사이트 몇 개만 수집하는 것인지, 아니면 있는지도 몰랐던 사이트에 방문하는 크롤러가 필요한 것인지 질문한다.
- 크롤러가 특정 웹사이트에 도달했을 때, 사이트의 정보를 탐색할지 다른 링크를 따라갈지 고려한다.
- 제외할 사이트는 없는지 고려한다. 예를 들어, 언어권이 다른 경우나 특정 컨텐츠를 포함하면 재귀를 종료할만한지 고려한다.
- 방문할 가능성이 있는 웹사이트에 크롤러가 방문하는 것이 합법적인지 고려한다.

### 3.2. Writing Web Crawler
웹 크롤러의 코드는 전체 사이트를 탐색하는 코드와 유사하다. 다만 탐색 한계를 명시하고 예외 사항을 처리해야 실무에 활용할 수 있다.

![](img/flow-of-crawler.png)

Flow of a crawler searching every outer link of a website.

위는 웹 크롤러 논리의 한 예이다. 크게 두 개의 루프가 있다고 할 때, 아래의 루프는 페이지 내의 외부 링크를 탐색하고, 외부 링크가 없는 경우에는 내부 링크를 탐색하여 리스트에 추가한다.


# Crawl with BeautifulSoup Library
## Concepts
<hr>

### 1. Analyzing Basic HTML

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("https://www.pythonscraping.com/pages/page1.html")
bs = BeautifulSoup(html.read(), 'html.parser')
print(bs.tag.subTag) # tag, subTag는 가상의 태그.
```

### `BeautifulSoup()`의 인자들
- 첫번째로 HTML 텍스트를 전달한다.
- 두번째로 BeautifulSoup가 객체를 만들때 쓰는 구문 분석기(parser)를 전달한다.
    ![](img/parsers.png)
    - `html.parser` : 별도의 C 패키지 설치 없이 사용할 수 있는 분석기
    - `lxml` : 형식을 지키지 않은 HTML 코드를 분석할 때 `html.parser`보다 나은 성능을 보인다.
    - `html5lib` : `lxml`보다 다양한 에러를 수정할 수 있다. 닫히지 않은 태그, 계층 구조가 잘못된 태그를 일일이 수정한다.

### 신뢰할 수 있는 연결
- `urlopen()`에서 등장할 수 있는 에러
    - 페이지를 찾을 수 없거나("404 Page Not Found"), URL 해석에서 에러가 생긴 경우("URLError")
    - 서버를 찾을 수 없는 경우("500 Internal Server Error")
    - `try ... except` 구문을 통해 예외를 처리한다.

```python
from urllib.request import urlopen
from urlib.error import HTTPError, URLError

try:
    html = urlopen('https://pythonscrapingthisurldoesnotexist.com')
except HTTPError as e:
    print(e)
except URLError as e:
    print('The server could not be found!')
else:
    print('Got HTML successfully.')
```

- `bs.tag.subTag`에서 등장할 수 있는 에러
    - BeautifulSoup는 존재하지 않는 태그에 접근을 시도하면 None 객체를 반환한다. 이때 None 객체에 대해 태그에 접근하려고 하면 AttributeError가 일어난다.
    - 두 개의 태그의 존재 유무를 명시적으로 체크한다.

```python
try:
    badContent = bs.tag.subTag
except AttributeError as e: # tag1이 존재하지 않는 경우
    print('tag was not found.')
else:
    if badContent == None:
        print('subTag was not found.')
    else:
        print(badContent)
```

### 고급 HTML 분석을 사용하지 않는 방법
- 더 나은 HTML 구조를 갖춘 모바일 버전 사이트 찾아보기
- 자바스크립트 파일을 불러와 분석하기
- URL에 원하는 정보가 있는지 찾아보기
- 원하는 정보를 다른 소스에서 가져올 수 있는지 고려하기

### Objects in BeautifulSoup
1. BeautifulSoup 객체 : 파싱된 문서 전체를 의미한다.
2. Tag 객체 : XML 또는 HTML 태그를 의미한다.
3. NavigableString 객체 : 태그가 아니라 태그 안에 있는 텍스트를 의미한다.
4. Comment 객체 : HTML 주석을 의미한다.

### find()와 findAll() 메서드 인자들
- find(tag, attributes, recursive, text, keywords)
- findAll(tag, attributes, recursive, text, limit, keywords)

- `tag` : 태그 이름인 문자열 또는 태그 이름 리스트를 넘긴다.
    ```python
    bs.findAll({'h1', 'h2', 'h3', 'h4', 'h5'})
    ```
- `attributes` : 속성으로 이루어진 파이썬 딕셔너리를 받고, 그 중 하나에 일치하는 태그를 모두 찾는다.
    ```python
    bs.findAll('span', {'class': {'green', 'red'}})
    ```
- `recursive` : 불리언으로, True이면 매개변수에 일치하는 자식과 자식의 자식을 검색하며 False이면 최상위 태그에 대해서만 검색한다.
- `text` : 태그의 속성이 아니라 텍스트 콘텐츠에서 일치하는 점을 검색한다.
    ```python
    nameList = bs.findAll(text='the prince')
    ```
- `limit` : 페이지의 항목을 처음부터 몇번 탐색할 것인지 지정한다. `find('')`는 `findAll('', limit=1)`과 같다.
- `keyword` : 특정 속성이 포함된 태그를 AND 연산으로 검색한다.
    ```python
    bs.findAll('', {'id':'text', 'class':'green'})
    ```
    - 주어진 조건을 모두 만족하는 태그 목록을 반환한다. 

## Tools for Crawling
<hr>

### Utilizing CSS
- CSS는 HTML 요소를 구분해 서로 다른 스타일을 적용하므로 웹 스크레이퍼에 도움이 된다.

    ```python
    nameList = bs.findAll('span', {'class':'green'})
    for name in nameList:
        print(name.get_text())
    ```
    위 코드는 `<span class="green"></span>` 태그에 들어있는 텍스트만 선택해서 파이썬 리스트로 추출한다.
- `get_text()`는 모든 태그를 제거한 유니코드 텍스트 문자열을 반환한다. 일반적으로 문서의 태그 구조를 유지하는 것이 바람직하므로 최종 데이터 출력 또는 저장 직전에 사용해야 한다.

### Utilizing Tree Navigation
1. 자식(children)과 자손(descendants) 다루기
    - 자식은 부모보다 한 태그 아래에 있고, 자손은 조상보다 하위 단계에 있는 모든 태그이다. BeautifulSoup는 항상 선택된 태그의 자손을 다룬다.
    - 자식만 찾을 때는 `.contents` 또는 `.children`을 사용한다. 전자는 리스트를 반환하며, 후자는 iterator를 반환한다.
    ```python
    for child in bs.find('span', {'class':'green'}).children:
        print(child)
    ```
2. 형제(sibling) 다루기
    - 테이블에서 데이터를 구할 때, 특히 테이블에 타이틀 행이 있는 경우 유용하게 활용할 수 있다. `.next_siblings`은 해당 객체를 제외한 다음 형제만 가져온다. 즉, 타이틀 행을 선택하면 그 타이틀 행을 제외한 모든 테이블 행을 가져온다.
    ```python
    for sibling in bs.find('span', {'class':'green'}).next_siblings:
        print(sybling)
    ```
3. 부모(parents) 다루기
    - 태그의 부모를 검색하기 위해 `.parent` 또는 `.parents`를 활용한다.
    ```python
    print(bs.find('img', {'src':'../img/gifts/img1.jpg'})).parent.previous_sibling.get_text()
    ```

### Utilizing Regular Expression
정규 표현식은 BeautifulSoup 표현식 어디든 매개변수로 삽입할 수 있다. 

예를 들어 `<img src='../img/gifts/img3.jpg'>` 형태의 제품 이미지를 여러개 찾는 것이 목표라고 하자. 이때 `findAll('img')`로 모든 이미지 태그를 가져올 시에 페이지의 불필요하거나 빈 이미지, 숨은 이미지들을 모두 가져오게 된다. 따라서 제품 이미지만 가져오기 위해 위의 제품 이미지 형태를 정규 표현식으로 전달할 수 있다.

```python
images = bs.findAll('img', {'src':re.compile('\.\.\/img\/gifts/img.*\.jpg')})
for image in images:
    print(image['src'])
```

### Utilizing Lambda Expression
특정 타입의 함수를 findAll 함수의 매개변수로 넘길 수 있다. 이 함수들은 태그 객체를 매개변수로 받고 불리언만 반환해야 한다. BeautifulSoup는 모든 태그 객체를 이 함수에서 평가하고, True로 평가된 태그만 반환한다.

예를 들어 다음 코드는 속성이 두개인 태그만 가져온다.
```python
bs.findAll(lambd tag: len(tag.attrs) == 2)
```

다음 코드는 `text` 기능을 lambda 함수로 표현한 예이다.
```python
bs.findAll(lambda tag: tag.get_text() == 'the prince')
```

## Reference
- 『Web Scraping with Python』, Ryan Mitchell
