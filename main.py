import uvicorn
import db
import parser as p
import api
import logging
import time
import multiprocessing as mp

# logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

app = api.app


def first():
    log.info('First thing running')
    # Get all news for today
    li = p.get_all_news()
    for n in li:
        if db.in_base(n.link):
            continue
        else:
            db.InsertNews(n.name, n.text, n.link, n.time)


def check():
    log.info('Check running')
    li = p.get_last_news()
    for n in li:
        db.InsertNews(n.name, n.text, n.link, n.time)
#

def server():
    log.info('Server running')
    uvicorn.run(
        "main:app",
        host='0.0.0.0',
        port=8000,
        reload=True
    )


def bgtasks():
    first()
    while True:
        check()
        time.sleep(3600)


if __name__ == '__main__':
    p3 = mp.Process(target=bgtasks)
    p3.start()
    p2 = mp.Process(target=server)
    p2.start()
    p3.join()
    p2.join()
