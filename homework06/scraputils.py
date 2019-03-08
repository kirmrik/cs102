import requests
from bs4 import BeautifulSoup
import time


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    tbl_list = parser.table.findAll('table')
    title_list = tbl_list[1].find_all("a", attrs={"class": "storylink"})
    url_list = ['https://news.ycombinator.com/' + title.get('href') if title.get('href').startswith('item?') else title.get('href') for title in title_list]
    title_list = [title.text for title in title_list]
    sub_list = tbl_list[1].find_all("td", attrs={"class": "subtext"})
    user_list = [sub.text.split()[3] for sub in sub_list]
    point_list = [int(sub.text.lstrip('\n').split()[0]) for sub in sub_list]
    comment_list = []
    for sub in sub_list:
        try:
            comment_list.append(int(sub.text.split()[-2]))
        except:
            comment_list.append(0)
    for user, comment, point, title, url in zip(
        user_list, comment_list, point_list, title_list, url_list
        ):
        new = {}
        new['author'] = user
        new['comments'] = comment
        new['points'] = point
        new['title'] = title
        new['url'] = url
        news_list.append(new)
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    tbl_list = parser.table.findAll('table')
    title_list = tbl_list[1].find_all("a", attrs={"class": "morelink"})
    next_page = title_list[0].get('href')
    return next_page


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    i = 0
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        print(response.ok, response.status_code)
        if not response.ok:
            i += 1
            pause = (2 ** i) * 0.5
            time.sleep(pause)
            continue
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
        i = 0
    return news

