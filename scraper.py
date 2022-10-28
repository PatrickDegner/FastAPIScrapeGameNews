from genericpath import exists
import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape():
    url = 'https://www.giga.de/news/'
    resp = requests.get(url)
    html = resp.text
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('article')

    df_new = pd.DataFrame(columns=['update_timestamp', 'title', 'news'])
    for article in articles:
        datetime = article.find('span', class_='alice-datetime').text
        title = article.find('h2').text
        text = article.find('p').text
        df_new = df_new.append({'update_timestamp': datetime,
                        'title': title, 'news': text}, ignore_index=True)

    df_new['update_timestamp'] = pd.to_datetime(df_new['update_timestamp'])
    if not exists('giga_news.csv'):
        df_new.to_csv('giga_news.csv', index=False)

    df_old = pd.read_csv('giga_news.csv')
    df_old['update_timestamp'] = pd.to_datetime(df_old['update_timestamp'])
    df_old = df_old.sort_values(by='update_timestamp', ascending=False)

    if df_new['update_timestamp'][0] > df_old['update_timestamp'][0]:
        df_new = df_new.append(df_old, ignore_index=True)
        df_new = df_new.drop_duplicates(subset=['title'])
        df_new.to_csv('giga_news.csv', index=False)
        print('new news found and got appended to csv...')
    else:
        print('no new news found... skipping...')

if __name__ == '__main__':
    scrape()
