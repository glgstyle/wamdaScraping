import sys
import os
import requests
from bs4 import BeautifulSoup
import csv

# Part1: Get infos from article link

# sys.argv -> list arguments passed to the script by the terminal (here the article url)
url =  sys.argv[1]
response = requests.get(url)
parser = BeautifulSoup(response.content,'html.parser')
article = (parser.find('div', class_='c-article'))
data = []

# title
title = article.find('h2', class_='c-article__title').string
data.append(title)

# content
div_content = article.find('div', class_='s-content')
# # if div_content exists
if div_content:
    # Use join() to concatenate all paragraphes to one string
    content = ' '.join(paragraph.get_text(strip=True) for paragraph in div_content.find_all('p'))
    # Add content to data
    data.append(content)

# date
date = article.find('p', class_='c-article__meta').time.string
data.append(date)

# tags
tags = ', '.join([tag.a.string for tag in article.find('ul', class_='c-tag-list').find_all('li')])
# Use join() method to reformat blog links in string not list['', '']
# reformat = '\n'.join(tags)
# data.append(reformat)
data.append(tags)


# blog_links (without javascript word)
blog_links = ', '.join([link.get('href') for link in article.find_all('a') if link.get('href') and link.get('href') != 'javascript:;'])
data.append(blog_links)

# creating file output
# Try to open data, if there is no directory create it
path = 'data'
try:
    os.makedirs(path)
except os.error:
    if not os.path.isdir(path):
        os.mkdir(path)

# output file article layout
header = ['Titre', 'Contenu du blog', 'Date', 'Tags', 'Liens dans le blog']

with open('data/data_article.csv', 'w', encoding='utf-8') as article:
    w = csv.writer(article, delimiter=',')
    w.writerow(header)
    w.writerow(data)
