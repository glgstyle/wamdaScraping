from tools import search_pagination, get_all_datas_articles_from_article_links


# Part3: Get all articles infos from all articles links

blog_url = "https://www.wamda.com/media"


# find_all_articles_from_blog(blog_url)
pagination = search_pagination(blog_url)
get_all_datas_articles_from_article_links(pagination)