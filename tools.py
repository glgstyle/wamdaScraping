import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from requests.exceptions import InvalidSchema
import csv
import re


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


def get_article_infos(url):
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

    # BLOG LINKS (without javascript word)
    try:
        blog_links = ', '.join([link.get('href') for link in article.find_all('a') if link.get('href') and link.get('href') != 'javascript:;'])
    except AttributeError:
        blog_links = ""
    data.append(blog_links)

    return data


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
    # If UlPager not empty
    if ulPager:
        r = session.get(baseUrl)
        try:
            # reduce the number of pages for tests
            # for i, html in enumerate(r.html):
            #     print(html.url)
            #     if i >= 10:
            #         break
            #     pages.append(html.url)

            for html in r.html:
                # print(html.url)
                pages.append(html.url)
        except InvalidSchema:
            print("Invalid schema encountered. Skipping this URL.")
    else:
        pages.append(baseUrl)
    return pages


def get_all_datas_articles_from_article_links(pagination):
    """Extracts all articles URLs from the provided page URL using pages links,
       get all datas of blog articles.

    Args:
        pagination (str): The pages URL of the website.

    Returns:
        list: A list of URLs of all articles on the website.
    """
    blog_titles_url = []

    # Header layout
    header = ['Titre', 'Contenu du blog', 'Date', 'Tags', 'Liens dans le blog']

    # Open output file with writing rights
    with open('data/all_articles_infos.csv', 'w', encoding='utf-8', newline='') as output_file:
        w = csv.writer(output_file, delimiter=',')
        # Write header
        w.writerow(header)
        # Loop on every page to find articles links
        for page in pagination:
            resp = requests.get(page)
            next_soup = BeautifulSoup(resp.content, 'html.parser')
            next_soup_article = next_soup.find_all('article', class_='c-media')

            # For each article in all articles extract the link, insert to blog_titles_url, get datas or article and write in output file
            for article in next_soup_article:
                article_link = article.h2.a.get('href')
                blog_titles_url.append(article_link)
                # print(article_link)
                article_datas = get_article_infos(article_link)
                w.writerow(article_datas)

            # Join all links in one string with ', ' as separator
            links_concatenated = ', '.join(blog_titles_url)

            # Add the string to blog_titles_url
            blog_titles_url = [links_concatenated]
    # print(blog_titles_url)
    return blog_titles_url
