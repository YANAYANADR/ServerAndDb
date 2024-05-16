from fastapi import FastAPI
import db
import logging

# logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
app = FastAPI()



@app.get("/")
async def read_root():
    log.info(f'Main page accessed')
    return {"Ids": db.get_all_ids()}


@app.get("/news/{id}/")
async def get_news_by_id(id: int):
    log.info(f'Id seen - {id}')
    return {'id': id,
            'name': db.get_by_id(id).name,
            'date': db.get_by_id(id).date,
            'text': db.get_by_id(id).text
            }
