import psycopg2  # Cant use 3rd because scram auth
from sqlalchemy import create_engine, String, text, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
import logging

# logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Creates db if not exists
engine = create_engine("postgresql://postgres:1234@db:5432/postgres",
                       isolation_level="AUTOCOMMIT")
with Session(engine) as sess:
    try:
        sess.execute(text('CREATE DATABASE yournews'))
        log.info('База создана')
    except Exception as e:
        log.info(f'База уже существует,{e}')

# Actual connection
engine = create_engine("postgresql://postgres:1234@db:5432/yournews")


class Base(DeclarativeBase):
    pass


class News(Base):
    __tablename__ = "news"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    text: Mapped[str] = mapped_column(String())
    link: Mapped[str] = mapped_column(String(200))
    # TODO FIX DATE
    date: Mapped[[str]] = mapped_column(String(200))


Base.metadata.create_all(engine)


# Methods
def InsertNews(name, text, link, date):
    with Session(engine) as s:
        art = News(name=name, text=text, link=link, date=date)
        s.add(art)
        s.flush()  # ?? idk
        s.commit()


def in_base(link):
    with Session(engine) as s:
        return len(s.execute(select(News).where(News.link == link)).all()) > 0


def get_by_id(id):
    with Session(engine) as s:
        res = s.execute(select(News).where(News.id == id)).all()[0][0]
        return res


def get_all_ids():
    with Session(engine) as s:
        res = s.execute(select(News.id)).all()
        return [a[0] for a in res]
