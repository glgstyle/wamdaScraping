import sys
import os
import requests
from bs4 import BeautifulSoup
import csv
import re


# Part1: Get infos from article link

# sys.argv -> list arguments passed to the script by the terminal (here the article url)
url =  sys.argv[1]


def clean_text(text):
    """
    Cleans text by removing non-ASCII characters and potentially other unwanted elements.

    Args:
        text (str): The text to be cleaned.

    Returns:
        str: The cleaned text.
    """
    # Regular expression for non-ASCII characters
    pattern = re.compile(r'[^\x00-\x7F]+')

    # Remove non-ASCII characters and normalize whitespace
    cleaned_text = re.sub(pattern, ' ', text).strip()

    return cleaned_text


def find_article_infos(url):
    """
    Fetches article information from a given URL.

    Args:
        url (str): The URL of the article.

    Returns:
        list: data containing the extracted informations.
    """
    response = requests.get(url)
    parser = BeautifulSoup(response.content,'html.parser')
    article = (parser.find('div', class_='c-article'))
    data = []

    # TITLE
    try:
        title = clean_text(article.find('h2', class_='c-article__title').string.strip())
    except AttributeError:
        title = ""
    data.append(title)

    # CONTENT
    try:
        div_content = article.find('div', class_='s-content')
        # if div_content exists
        if div_content:
            # Initialise a list to stock each paragraph text
            paragraphs_text = []
            # Looping to the paragraphs in div_content
            for paragraph in div_content.find_all('p'):
                # Add paragraph to the list
                paragraph_text = paragraph.get_text(strip=True)
                if paragraph_text:
                    paragraphs_text.append(paragraph_text)
            # Concatenate all paragraphs in one string by separating them with line break
            content = '\n'.join(paragraphs_text)
            # Clean all line break by concatenate text
            content_cleaned = content.replace('\n', '')
        else:
            content_cleaned = ""
    except AttributeError:
        content_cleaned = ""

    # Clean the text before to append in data
    cleaned_text = clean_text(content_cleaned)

    # Add cleaned text to data
    data.append(cleaned_text)     
        
    # DATE
    try:
        date = article.find('p', class_='c-article__meta').time.string
    except AttributeError:
        # Record empty date if no date in article
        date = ""
    data.append(date)

    # TAGS
    try:
        ul_element = article.find('ul', class_='c-tag-list')
        if ul_element is not None:
            tags = ', '.join([tag.a.string for tag in ul_element.find_all('li') if tag.a.string is not None])
        else:
            tags = ""  # Assign an empty string if the element is not found
    except AttributeError:
        tags = ""
    clean_tags = clean_text(tags)
    data.append(clean_tags)

    # BLOG_LINKS (without javascript word)
    try:
        blog_links = ', '.join([link.get('href') for link in article.find_all('a') if link.get('href') and link.get('href') != 'javascript:;'])
    except AttributeError:
        blog_links = ""
    data.append(blog_links)

    return data

# OUTPUT FILE
# Try to open data, if there is no directory create it
path = 'data'
try:
    os.makedirs(path)
except os.error:
    if not os.path.isdir(path):
        os.mkdir(path)

# Header layout
header = ['Titre', 'Contenu du blog', 'Date', 'Tags', 'Liens dans le blog']

# Open file with writing rights to write header and datas
with open('data/data_article.csv', 'w', encoding='utf-8') as article:
    w = csv.writer(article, delimiter=',')
    w.writerow(header)
    w.writerow(find_article_infos(url))
