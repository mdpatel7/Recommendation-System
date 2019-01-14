import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

list = []

def decomposeDiv(soup):
    for collapsible_div in soup.find_all('div', class_='collapsible'):
        collapsible_div.decompose()

def contentFromLink(a_link,link):
    # print(a_link)
    global list
    page_title = link.get_text()
    # print(title)
    urlPage = requests.get(a_link)
    soup = BeautifulSoup(urlPage.content,'html.parser')
    div = soup.find('div', {'id':'mw-content-text'})
    all_tags = div.find('p').next_siblings
    # print(all_tags)
    for required_tags in all_tags:
        dict = {}
        # print(required_tags.name)
        if required_tags.name == 'h2':
            page_title = required_tags.text
            data = ''
            type_of_data = ''
        elif required_tags.name == 'p' or required_tags.name == 'ul li'or required_tags.name == 'li' or required_tags.name == 'pre':
            data = required_tags.text
            type_of_data = 'plain_text'
        elif required_tags.name != None and required_tags.find('div', class_='mw-highlight mw-content-ltr') is not None:
            data = required_tags.find('div', class_='mw-highlight mw-content-ltr').text
            type_of_data = 'code_fragment'
        else:
            continue

        dict['Page Title'] = page_title
        dict['Data'] = data
        dict['Type Of Data'] = type_of_data
        list.append(dict)

def getJavaWikiBookContent(url):
    page = requests.get(url)
    # print(page.status_code)
    soup = BeautifulSoup(page.content, 'html.parser')
    div = soup.find('div', class_='mw-parser-output')
    decomposeDiv(soup)
    i = 0
    all_ul = div.find_all("ul")
    for each_ul in all_ul:
        all_li = each_ul.find_all("li")
        for each_li in all_li:
            all_ahref = each_li.find_all("a", href=re.compile("Java_Programming"))
            for each_href in all_ahref:
                i = i+1
                if i== 69 or i== 70 or i == 71 or i== 72 \
                        or i == 74 or i == 75 or i == 76 or i == 77:
                    break
                a_link = "https://en.wikibooks.org"+each_href.get('href')
                # print(a_link)
                # title = link.get_text('title')
                # print(title)
                contentFromLink(a_link,each_href)
    df = pd.DataFrame.from_dict(list)
    df.to_csv('content.csv')


getJavaWikiBookContent("https://en.wikibooks.org/wiki/Java_Programming")
