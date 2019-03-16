from scraputils import get_news
from db import News, session

if __name__ == "__main__":
    news = get_news("https://news.ycombinator.com/newest", 34)
    s = session()
    for new in news:
        record = News(title=new['title'],
                      author=new['author'],
                      url=new['url'],
                      comments=new['comments'],
                      points=new['points'])
        s.add(record)
    s.commit()
