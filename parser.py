from collections import namedtuple
import requests
from bs4 import BeautifulSoup
import datetime
import db  # probably shouldn't
import logging

#logging
logging.basicConfig(level=logging.INFO)
log=logging.getLogger(__name__)

# get named tuple
art_tuple = namedtuple("article", "link name time text")


def get_all_news():
    all = []
    r = requests.get('https://uralpolit.ru/')
    html = BeautifulSoup(r.text, features="html.parser")
    f = False
    for li in html.select('.col-xs-10.col-md-4 li'):
        art = li.find('article')
        # Check for date to stop
        if not art:
            if f:
                log.info('Конец сегодняшних новостей')
                break
            else:
                f = True
                continue
        # Values
        link = art.find('a', class_='news-article__title').get('href')
        name = art.find('a', class_='news-article__title').get_text()
        time = (datetime.datetime.today().strftime('%Y-%m-%d') +
                ' ' + art.time.get_text() + ':00')
        conReq = requests.get('https://uralpolit.ru/' + link)
        text = (BeautifulSoup(conReq.text, features="html.parser")
                .find(id='to_hypercomments_area').get_text()).replace('\n', '').replace('\r', '')
        all.append(art_tuple(link, name, time, text))
    return all


# this gets all new ones and stops if it sees a familiar link
def get_last_news():
    all = []
    r = requests.get('https://uralpolit.ru/')
    html = BeautifulSoup(r.text, features="html.parser")
    f = False
    for li in html.select('.col-xs-10.col-md-4 li'):
        art = li.find('article')
        # Check for date to stop
        if not art:
            if f:
                break
            else:
                f = True
                continue
        # Values
        link = art.find('a', class_='news-article__title').get('href')
        if db.in_base(link):
            log.info('Дошли до ссылки, которая уже в базе')
            break
        name = art.find('a', class_='news-article__title').get_text()
        time = (datetime.datetime.today().strftime('%Y-%m-%d') +
                ' ' + art.time.get_text() + ':00')
        con_req = requests.get('https://uralpolit.ru/' + link)
        text = (((BeautifulSoup(con_req.text, features="html.parser")
                .find(id='to_hypercomments_area').get_text()).
                replace('\n', '').replace('\r', ''))
                .replace('\t',''))
        all.append(art_tuple(link, name, time, text))
    return all
