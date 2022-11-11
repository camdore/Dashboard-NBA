from base64 import encode
from re import A, X
from turtle import shape
import urllib.request
from html.parser import HTMLParser
import pandas as pd
from attr import attr


url = 'https://www.basketball-reference.com/leagues/NBA_2019_shooting.html'
url2 = 'https://www.basketball-reference.com/leagues/NBA_2019_totals.html'
url3_17_18 = 'https://www.basketball-reference.com/leagues/NBA_2018_totals.html'

data = pd.read_html(url3_17_18, flavor='lxml' )[0]
print(data)
print(type(data))
# print(data.ndim)
# print(data.size)

df = pd.DataFrame(data)
csv_data = df.to_csv('csv_data_NBA_players_17_18.csv',encoding = 'utf8',index=False)

# print(type(df))
# print(df.shape)
# print(df)
# field_goals = df['FG']
# print(field_goals.values)
# print(field_goals.dtype)
