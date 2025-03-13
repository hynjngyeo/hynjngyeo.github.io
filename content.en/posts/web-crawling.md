+++
title = "Web Crawling with Python"
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

<!DOCTYPE html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        h3::before {
            content: "📌 ";
        }
    </style>
</head>

This post summarizes the key takeaways from my reading of _Web Scraping with Python_ by Ryan Mitchell. The code examples included have been tested locally.

Web crawling recursively finds URLs on a page and repeatedly loads new pages. While a scraper works well when all data is contained within a single page, using a crawler requires careful attention to bandwidth to minimize the load on the target server.

# Quick Approach
<hr style="border: 1px solid; margin-top: -5px;">

Here are some basic techniques that can scrape and crawl single web page, web site, and the Internet.

{{% hint info %}}
**Before Building a Crawler**  
For effective crawling, especially for large scale project, check in advance if the data is obtainable through API. Using APIs to retrieve data is generally more efficient in terms of speed: APIs impose less strain on the target server as they provide data in a controlled and optimized manner. 

For example, Wikipedia provides [Wiki API](https://www.mediawiki.org/wiki/API:Main_page).
{{% /hint %}}

## 1. Scraping a Web Page
<hr>

Let's write a program that scrapes HTML text from Wikipedia. Following code collects a link list from a specifice Wikipedia web page.

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


## 2. Crawling a Web Site
<hr>

### Questions to Answer

1. **Is the webpage scrapable?**
    - **Surface Web** refers to the web stored in search engines.
    - **Deep Web** is the rest part of the surface web, accounting for 90% of the Internet. Deep Web includes unliked pages and pages blocked with `robots.txt`, with some of them are scrapable.
        - `robots.txt` is a file used to control web crawler access, specifying which parts of a website should or should not be crawled.
    - **Dark Web** is part of the deep web which requires a specific program or method to access such as _Tor_. A different approach is required to scrap the dark web compared to the surface web.
        - Tor(The Onion Router) is a software and network that enables anonymization by routing traffic through multiple encrypted relays.

2. **When to scrape an entire site?**
    - **Sitemap Generation**: By navigating the entire site through a crawler and collecting internal links, pages can be organized similarly to a folder structure. This process helps estimate website design costs.
    - **Data Collection**: Recursive crawling can be used to create a prototype of a search platform, even when limited to specific pages such as blog posts or news articles.

### Preventing Duplicate Crawling 
Suppose a website consists of five levels, with each page containing ten internal links. To thoroughly explore the site, a crawler needs to scan at least $105$ pages and, in the worst case, up to $10^5$ pages. However, due to significant redundancy among internal links, the need to crawl $10^5$ pages is rare.

Thus, it is crucial for a web crawling program to **avoid redundant visits**. To prevent crawling the same page twice, discovered internal links should follow a **consistent format** and be stored in a **set (Set data structure)** to ensure uniqueness.

```python
# To avoid obtaining data from the same web page, manage visited links in a set.
pages = set()

def printLinks(pageUrl, recur_cnt):
    """
    Perform recursive traversal `recur_cnt` times in Wikipedia site.
    """
    # Limit recursion limit to 100.
    recur_cnt += 1
    if recur_cnt > 100: return

    # Define a set to persist throughout the program's execution.
    global pages
    
    # Search for `pageUrl` in Wikipedia.
    try:
        html = urlopen(f'http://en.wikipedia.org/{pageUrl}')
    except HTTPError as e:
        print(e)
    except URLError as e:
        print('The server could not be found!')
    else:
        print('Got HTML successfully.')

    bs = BeautifulSoup(html.read(), 'html.parser')

    # Pring every 'wiki/...' URLs in the page.
    for link in bs.findAll('a', href=re.compile('^('wiki/')')):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                # Search for a new page.
                newPage = link.attr['href']
                print(newPage)
                pages.add(newPage)
                printLinks(newPage)

# Call printLinks function iteratively.
# NOTE: Be mindful of memory usage when setting the iteration.
printLinks('', 1)
```

### Collecting Data from the Entire Site
Now you can collect data from the entire site with the code below.

```python
pages = set()

def printSummary(pageUrl, recur_cnt):
    """
    Print page title, first paragraphm and edit link by searching
    inner links in the Wikipedia site.
    """
    recur_cnt += 1
    if recur_cnt > 100: return

    global pages
    html = urlopen(f'http://en.wikipedia.org/{pageUrl}')
    bs = BeautifulSoup(html.read(), 'html.parser')

    try: # Is a content page if below are executed.
        # Print the title.
        print(bs.h1.get_text())
        # Print the first paragraph.
        # Select the first element from div#mw-content-text -> p.
        print(bs.find(id='mw-context-text').findall('p')[0])
        # Print the edit link.
        # Search for li#ca-edit -> span -> a.
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

## 3. Crawling the Internet
<hr>

### Questions to Answer
- Ask whether the crawler should collect data from a predefined set of sites or explore unknown sites as well.
- Determine whether the crawler should analyze the content of a website upon reaching it or follow links to other pages.
- Consider if there are any sites to exclude. For example, should recursion stop when encountering a different language or specific content?
- Ensure that visiting potential websites with the crawler is legally permissible.

### Building a Web Crawler
The code for a web crawler is similar to that of a full-site exploration script. However, to make it practical for real-world applications, it must define exploration limits and handle exceptions properly.

Below is an example of a web crawler flow. Assuming there are two main loops, the following loop explores external links on a page. If no external links are found, it searches for internal links and adds them to a list.

<figure>
    <img src="/posts/images/crawler-flow.png" width="100%">
    <figcaption>Flow of a crawler searching every outer link of a website.</figcaption>
</figure>



<br>

# Crawl with BeautifulSoup Library
<hr style="border: 1px solid; margin-top: -5px;">

Let's dive in to further concepts and tools in python library, BeautifulSoup -- which helps parsing and extracting data from HTML and XML documents. It provides simple methods to navigate, search, and modify the parsed tree. Here, it can be used for obtaining targeted information from websites.

## 4. BeautifulSoup Basics
<hr>

### Objects & Parsers

#### Main Objects in BeautifulSoup  
1. **`BeautifulSoup`**: Represents the entire parsed document.  
2. **`Tag`**: Represents an individual XML or HTML tag.  
3. **`NavigableString`**: Represents the text inside a tag, excluding the tag itself.  
4. **`Comment`**: Represents an HTML comment.  

#### Parsers in BeautifulSoup  
- **`html.parser`**: A built-in parser that requires no additional C package installation.  
- **`lxml`**: Provides better performance than `html.parser` when parsing malformed HTML.  
- **`html5lib`**: More robust than `lxml`, automatically fixing unclosed tags and incorrect tag hierarchies.  

Following code shows how to read basic html components with `BeautifulSoup()`.
```python
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("https://www.pythonscraping.com/pages/page1.html")
bs = BeautifulSoup(html.read(), 'html.parser')
print(bs.tag.subTag) 
```
1. First, pass the HTML text.  
2. Second, pass the parser that BeautifulSoup uses to create an object.  


### Method `find()` and `findAll()`
> - `find(tag, attributes, recursive, text, keywords)`
> - `findAll(tag, attributes, recursive, text, limit, keywords)`

- **`tag`**: Accepts a string or a list of tag names to search for.  
    ```python
    bs.findAll({'h1', 'h2', 'h3', 'h4', 'h5'})
    ```  
- **`attributes`**: Takes a Python dictionary of attributes and finds all tags that match any of them.  
    ```python
    bs.findAll('span', {'class': {'green', 'red'}})
    ```  
- **`recursive`**: A boolean value. If `True`, it searches through all descendants (children and sub-children). If `False`, it only searches the immediate children of the specified tag.  
- **`text`**: Searches for matching text content rather than tag attributes.  
    ```python
    nameList = bs.findAll(text='the prince')
    ```  
- **`limit`**: Specifies how many matches to return from the beginning of the search.  
  - `find('')` is equivalent to `findAll('', limit=1)`.  
- **`keyword`**: Searches for tags that contain specific attributes using an AND condition.  
    ```python
    bs.findAll('', {'id': 'text', 'class': 'green'})
    ```  
  - Returns a list of tags that satisfy all given conditions.  

### Approaches to a Reliable Connection
1. **Possible errors that may occur in `urlopen()`**
    - When the page cannot be found ("404 Page Not Found") or there is an error in URL parsing ("URLError").
    - When the server cannot be found ("500 Internal Server Error").
- Solution: Use a `try ... except` block to handle exceptions.
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

2. **Potential errors from `bs.tag.subTag`**
    - BeautifulSoup returns `None` when attempting to access a non-existing tag. If an attribute or method is accessed on a `None` object, an `AttributeError` occurs.
- Solution: Explicitly check for the existence of both tags.
    ```python
    try:
        badContent = bs.tag.subTag
    except AttributeError as e:
        print('tag was not found.')
    else:
        if badContent == None:
            print('subTag was not found.')
        else:
            print(badContent)
    ```

## 5. Tools for Crawling
<hr>

In case you want to obtain specific informations from website with complicated HTML sturcture, these tools might help. 

{{% hint info %}}
**Before utilizing these tools**, one may consider these methods before getting their hands dirty:
- Search for mobile version sites with better HTML structure.
- Search for the target information in URL or JavaScript file.
- Consider alternative sources for obtaining necessary information.
{{% /hint %}}

### Utilizing CSS  
CSS differentiates HTML elements and applies different styles, which helps web scrapers extract specific elements.  
```python
nameList = bs.findAll('span', {'class': 'green'})
for name in nameList:
    print(name.get_text())
```
The above code extracts and returns a Python list containing the text inside `<span class="green"></span>` tags.
- `get_text()` removes all tags and returns a Unicode text string. Since preserving the document’s tag structure is often desirable, it's best to use this method only when outputting or saving the final data.

### Utilizing Tree Navigation
1. Dealing with `children` and `descendants`
    - A **child** is one level below its parent tag, while **descendants** include all tags below their ancestor. BeautifulSoup primarily deals with descendants.
    - To find only children, use `.contents` or `.children`.
        - `.contents` returns a list, while `.children` returns an iterator.
    ```python
    for child in bs.find('span', {'class':'green'}).children:
        print(child)
    ```
2. Dealing with `sibling`
    - Useful for extracting table data, especially when a table has a title row.
    - `.next_siblings` retrieves only the following siblings, excluding the current object.
    - Selecting the title row allows retrieval of all subsequent table rows.
    ```python
    for sibling in bs.find('span', {'class':'green'}).next_siblings:
        print(sybling)
    ```
3. Dealing with `parents`
    - To find a tag's parent, use `.parent` or `.parents`.
    ```python
    print(bs.find('img', {'src':'../img/gifts/img1.jpg'})).parent.previous_sibling.get_text()
    ```

### Utilizing Regular Expression
Regular expressions can be used as parameters in any BeautifulSoup expression.  

For example, suppose we want to find multiple product images in the format: `<img src='../img/gifts/img3.jpg'>`. Using `findAll('img')` would retrieve all image tags on the page, including unnecessary, empty, or hidden images. To filter only product images, we can pass a regular expression that matches this specific image format.

```python
images = bs.findAll('img', {'src':re.compile('\.\.\/img\/gifts/img.*\.jpg')})
for image in images:
    print(image['src'])
```

### Utilizing Lambda Expression
Specific types of functions can be passed as parameters to the `findAll()` method. These functions must:
1. Accept a tag object as a parameter.
2. Return only a boolean (True or False).

BeautifulSoup evaluates each tag with this function and returns only those that evaluate to True. For example, the following code retrieves only tags that have exactly two attributes:
```python
bs.findAll(lambd tag: len(tag.attrs) == 2)
```

The following code is an example of expressing the text feature using a lambda function.
```python
bs.findAll(lambda tag: tag.get_text() == 'the prince')
```

<hr>

## Reference
- Web Scraping with Python, Ryan Mitchell
