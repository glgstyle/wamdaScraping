import requests
import os
import csv
from bs4 import BeautifulSoup
from tools import search_pagination, find_all_articles_from_links
# from scrap_article import get_article_infos
# from scrap_all_articles_links import search_pagination, find_all_articles_links


# Part3: Get all articles infos from all articles links
# blog_url = "https://www.wamda.com/media"

# def find_all_articles_from_blog(blog_url):
#     # pagination = search_pagination(blog_url)
#     # articles_links = find_all_articles_links(pagination)
#     articles_links = csv.reader('data/all_articles_links', delimiter=',')
#     # creating file output
#     # Try to open data, if there is no directory create it
#     path = 'data/all_articles_infos'
#     try:
#         os.makedirs(path)
#     except os.error:
#         if not os.path.isdir(path):
#             os.mkdir(path)

#     # output file article layout
#     header = ['Titre', 'Contenu du blog', 'Date', 'Tags', 'Liens dans le blog']
#     with open('data/all_articles_infos.csv', 'w', encoding='utf-8') as h:
#             w = csv.writer(h)
#             w.writerow(header)
#     if articles_links:
#         for article in articles_links:
#             print("*********Article", article)
#             article_datas = get_article_infos(article)
#             print(article_datas)
#             with open('data/all_articles_infos.csv', 'w', encoding='utf-8', newline='') as article:
#                 w = csv.writer(article, delimiter=',')
#                 # w.writerow(header)
#                 w.writerow(article_datas)

blog_url = "https://www.wamda.com/media"

# def find_all_articles_from_blog(blog_url):
    # Décommentez et implémentez ces fonctions pour récupérer les URL
    # search_pagination = search_pagination(blog_url)
    # articles_links = find_all_articles_links(pagination)
    # search_pagination = search_pagination(blog_url)
    # find_all_articles_links(search_pagination(blog_url))


# #     # output file article layout
#     header = ['Titre', 'Contenu du blog', 'Date', 'Tags', 'Liens dans le blog']

#     # Ouvrez le fichier de sortie une seule fois
#     with open('data/all_articles_infos.csv', 'w', encoding='utf-8', newline='') as output_file:
#         w = csv.writer(output_file, delimiter=',')

#         # Ecrivez l'en-tête uniquement une fois
#         w.writerow(header)

#         # Assurez-vous que articles_links contient des URL valides
#         for article_url in articles_links:
#             print("*********Article", article_url)
#             article_datas = get_article_infos(article_url)  # Assurez-vous que cette fonction existe
#             print(article_datas)
#             w.writerow(article_datas)

# find_all_articles_from_blog(blog_url)
pagination = search_pagination(blog_url)
find_all_articles_from_links(pagination)