import os
import pandas as pd

# test giga_news.csv exists
def test_giga_news_exists():
    assert os.path.exists('giga_news.csv')

# test giga_news.csv is not empty
def test_giga_news_not_empty():
    assert os.stat('giga_news.csv').st_size != 0

# test giga_news.csv has 3 columns
def test_giga_news_has_5_columns():
    assert len(pd.read_csv('giga_news.csv').columns) == 3

# test giga_news.csv has 10 or more rows
def test_giga_news_has_10_rows():
    assert len(pd.read_csv('giga_news.csv')) >= 10

