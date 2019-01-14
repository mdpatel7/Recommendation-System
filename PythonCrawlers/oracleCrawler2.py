import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

list = []


def getContentFromLinkLevel3(new_link_level2):
    urlPage = requests.get(new_link_level2)
    soup = BeautifulSoup(urlPage.content,'html.parser')
    title_div = soup.find('div',{'id':'PageTitle'})
    # print(title_div.text)
    page_title = title_div.text
    content_div = soup.find('div',{'id':'PageContent'})
    all_tags = content_div.find_all()
    # print(all_tags)
    for required_tags in all_tags:
        dict = {}
        if required_tags.name == 'h2':
            page_title = required_tags.text
            data = ''
            type_of_data = ''
        elif required_tags.name == 'p' or required_tags.name == 'ul' or required_tags.name == 'ol':
            data = required_tags.text
            type_of_data = 'plain_text'
        elif required_tags.name == 'div' and required_tags.find('pre') is not None:
            pre_tag = required_tags.find('pre')
            data = pre_tag.text
            type_of_data = 'code_fragment'
        else:
            continue

        dict['Page Title'] = page_title
        dict['Data'] = data
        dict['Type Of Data'] = type_of_data
        list.append(dict)



def getContentFromLink(a_link, each_href):
    urlPage = requests.get(a_link)
    # print(urlPage.status_code)
    soup = BeautifulSoup(urlPage.content, 'html.parser')
    # div = soup.find('div', class_='MainFlow_wide')
    div_inside_div = soup.find('div', class_='NavBit')
    all_a = div_inside_div.find_all('a')
    # print(all_a)
    a_link = a_link[:a_link.find('index.html')]
    i = 0;
    for each_a in all_a:
        # print(each_a.get('href'))
        if each_a.get('href') == './TOC.html' or each_a.get('href') == '../TOC.html':
            new_link = a_link + 'TOC.html'
            # print(new_link)
            urllevel2 = requests.get(new_link)
            new_link = new_link[:new_link.find('TOC.html')]
            soup2 = BeautifulSoup(urllevel2.content, 'html.parser')
            divlevel2 = soup2.find('div',{'id':'PageContent'})
            all_ul = divlevel2.find_all('ul')
            for each_ul in all_ul:
                all_li = each_ul.find_all('li')
                for each_li in all_li:
                    all_ahref = each_li.find_all('a')
                    for each_href in all_ahref:
                        new_link_level2 = new_link+each_href.get('href')
                        print(new_link_level2)
                        getContentFromLinkLevel3(new_link_level2)


def getOracleTutorialContent(url):
    page = requests.get(url)
    print(page.status_code)
    soup = BeautifulSoup(page.content, 'html.parser')
    div = soup.find('div', {'id': 'TutBody'})
    all_ul = div.find_all('ul')
    for each_ul in all_ul:
        all_li = each_ul.find_all('li')
        for each_li in all_li:
            all_href = each_li.find_all('a')
            # print(all_href)
            for each_href in all_href:
                if "https://docs.oracle.com/" not in each_href.get('href'):
                    a_link = "https://docs.oracle.com/javase/tutorial/" + each_href.get('href')
                    # print(a_link)
                    if a_link == 'https://docs.oracle.com/javase/tutorial/java/generics/index.html' or a_link == 'https://docs.oracle.com/javase/tutorial/extra/generics/index.html' or a_link == 'https://docs.oracle.com/javase/tutorial/extra/fullscreen/index.html' or a_link == 'https://docs.oracle.com/javase/tutorial/extra/certification/index.html':
                        continue
                    getContentFromLink(a_link, each_href)
                else:
                    a_link = each_href.get('href')
                    # print(a_link)
                    if a_link == 'https://docs.oracle.com/javafx/index.html':
                        continue
                    getContentFromLink(a_link, each_href)
    df = pd.DataFrame.from_dict(list)
    df.to_csv('contentFromOracle.csv')

getOracleTutorialContent("https://docs.oracle.com/javase/tutorial/")