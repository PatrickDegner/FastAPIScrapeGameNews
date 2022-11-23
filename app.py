from fastapi.templating import Jinja2Templates
from fastapi import FastAPI
import pandas as pd
import scraper

app = FastAPI()
templates = Jinja2Templates(directory='templates')


@app.get('/')
def index():
    scraper.scrape()
    df = pd.read_csv('giga_news.csv')
    df['update_timestamp'] = pd.to_datetime(df['update_timestamp'])
    df = df.sort_values(by='update_timestamp', ascending=False)
    return templates.TemplateResponse('index.html', {'request': df})


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=80)
