import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape():
    url = 'https://www.giga.de/news/'
    resp = requests.get(url)
    html = resp.text
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('article')

    df = pd.DataFrame(columns=['update_timestamp', 'title', 'news'])

    for article in articles:
        datetime = article.find('span', class_='alice-datetime').text
        title = article.find('h2').text
        text = article.find('p').text
        df = df.append({'update_timestamp': datetime,
                        'title': title, 'news': text}, ignore_index=True)

    df['update_timestamp'] = pd.to_datetime(df['update_timestamp'])
    df.to_csv('giga_news.csv', index=False)

    df_new = pd.read_csv('giga_news.csv')
    df_new['update_timestamp'] = pd.to_datetime(df_new['update_timestamp'])
    df_new = df_new.sort_values(by='update_timestamp', ascending=False)

    if df_new['update_timestamp'][0] > df['update_timestamp'][0]:
        df = df.append(df_new, ignore_index=True)
        df = df.drop_duplicates(subset=['title'])
        df.to_csv('giga_news.csv', index=False)
        print('New articles found and appended to csv')
    else:
        print('no new articles')


if __name__ == '__main__':
    scrape()
