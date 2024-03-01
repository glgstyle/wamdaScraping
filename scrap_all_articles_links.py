import requests
import os
import csv
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from requests.exceptions import InvalidSchema


# Part2: Get all articles links from all pages of blog

url = "https://www.wamda.com/media"


def search_pagination(baseUrl):
    """Extracts all page URLs from the provided base URL using pagination links.

    Args:
        base_url (str): The base URL of the website.

    Returns:
        list: A list of URLs of all pages on the website.
    """
    response = requests.get(baseUrl)
    soup = BeautifulSoup(response.content, 'html.parser')
    session = HTMLSession()
    ulPager = soup.find('ul', class_='c-pagination')
    pages = []
    # génère erreur javascript
    # si ul pager n'est pas vide
    if ulPager:
        r = session.get(baseUrl)
        try:
            for html in r.html:
                print(html.url)
                # if html.get("href").startswith("javascript:;"):
                pages.append(html.url)
        except InvalidSchema:
            print("Invalid schema encountered. Skipping this URL.")
    else:
        pages.append(baseUrl)
    print(pages)
    return pages


def find_all_articles_links(pagination):
    blog_titles_url = []
    # loop on every page to find articles links
    for page in pagination:
        resp = requests.get(page)
        next_soup = BeautifulSoup(resp.content, 'html.parser')
        # next_soup_articles = next_soup.find('div', class_='o-grid')
        next_soup_article = next_soup.find_all('article', class_='c-media')

        # for each article in all articles extract the link, insert to blog_titles_url
        for article in next_soup_article:
            link_to_article = article.h2.a.get('href')
            blog_titles_url.append(link_to_article)
            print(link_to_article)

        # join all links in one string with ', ' as separator
        links_concatenated = ', '.join(blog_titles_url)

        # Add the string to blog_titles_url
        blog_titles_url = [links_concatenated]
    print(blog_titles_url)
    return blog_titles_url

# def get_page_articles_infos(page_url):
#     all_page_articles_content = []
#     # loop on every page to find articles content
#     for article in page_url:
#         get_article_infos(page_url)
#         # creating file output
#         # Try to open data, if there is no directory create it
#         path = 'data/articles_infos'
#         try:
#             os.makedirs(path)
#         except os.error:
#             if not os.path.isdir(path):
#                 os.mkdir(path)

#         # output file article layout
#         header = ['Titre', 'Contenu du blog', 'Date', 'Tags', 'Liens dans le blog']

#         with open('data/data_article.csv', 'w', encoding='utf-8') as article:
#             w = csv.writer(article, delimiter=',')
#             w.writerow(header)
#             w.writerow(get_article_infos(url))


# creating file output
# Try to open data, if there is no directory create it
path = 'data'
try:
    os.makedirs(path)
except os.error:
    if not os.path.isdir(path):
        os.mkdir(path)

# output file article layout
header = ['Articles url']

with open('data/all_articles_links.csv', 'w', encoding='utf-8', newline='') as article:
    w = csv.writer(article, delimiter=',')
    w.writerow(header)
    pagination = search_pagination(url)
    w.writerow(find_all_articles_links(pagination))