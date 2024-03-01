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
    # If UlPager is not empty
    if ulPager:
        r = session.get(baseUrl)
        try:
            for html in r.html:
                # print(html.url)
                pages.append(html.url)
        except InvalidSchema:
            print("Invalid schema encountered. Skipping this URL.")
    else:
        pages.append(baseUrl)
    # print(pages)
    return pages


def find_all_articles_links(pagination):
    """Extracts all articles URLs from the provided page URL using pages links.

    Args:
        pagination (str): The pages URL of the website.

    Returns:
        list: A list of URLs of all articles on the website.
    """
    blog_titles_url = []
    # Loop on every page to find articles links
    for page in pagination:
        resp = requests.get(page)
        next_soup = BeautifulSoup(resp.content, 'html.parser')
        next_soup_article = next_soup.find_all('article', class_='c-media')

        # For each article in all articles extract the link, insert to blog_titles_url
        for article in next_soup_article:
            link_to_article = article.h2.a.get('href')
            blog_titles_url.append(link_to_article)
            # print(link_to_article)

        # Join all links in one string with ', ' as separator
        links_concatenated = ', '.join(blog_titles_url)

        # Add the string to blog_titles_url
        blog_titles_url = [links_concatenated]
    # print(blog_titles_url)
    return blog_titles_url


# FILE OUTPUT
# Try to open data, if there is no directory create it
path = 'data'
try:
    os.makedirs(path)
except os.error:
    if not os.path.isdir(path):
        os.mkdir(path)

# Header layout
header = ['Articles url']

# Open output file with writing rights
with open('data/all_articles_links.csv', 'w', encoding='utf-8', newline='') as article:
    w = csv.writer(article, delimiter=',')
    w.writerow(header)
    pagination = search_pagination(url)
    w.writerow(find_all_articles_links(pagination))