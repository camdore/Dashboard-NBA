from wsgiref import headers
from matplotlib.font_manager import json_load
import requests, json
import urllib.parse
from nba_api.stats.endpoints import shotchartdetail
import pandas as pd


# url_base = 'https://stats.nba.com/stats/shotchartdetail'
url_nba ='https://stats.nba.com/stats/shotchartdetail?AheadBehind=&ClutchTime=&ContextFilter=&ContextMeasure=PTS&DateFrom=&DateTo=&EndPeriod=&EndRange=&GameID=&GameSegment=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&Period=0&PlayerID=2544&PlayerPosition=&PointDiff=&Position=&RangeType=&RookieYear=&Season=&SeasonSegment=&SeasonType=Regular+Season&StartPeriod=&StartRange=&TeamID=1610612739&VsConference=&VsDivision='
headers = {
    'Host': 'stats.nba.com',
		'Connection': 'keep-alive',
		'Accept': 'application/json, text/plain, */*',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
		'Referer': 'https://stats.nba.com/',
		"x-nba-stats-origin": "stats",
		"x-nba-stats-token": "true",
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'en-US,en;q=0.9',
}
rt = requests.get(url_nba,headers=headers)
# print(type(rt))
# print(rt)
# print(rt.json)
json_data = json.loads(rt.text)
print(type(json_data))
print(json_data.keys())
print(json_data['resource'])
results = json_data['resultSets'][0]
col = results['headers']
rows = results['rowSet']

df = pd.DataFrame(rows)
col = df.columns

print(df)

# csv_data = df.to_csv('csv_data.csv',encoding = 'utf8',index=False)
# print(type(csv_data))
# excel_data = df.to_excel("nba_data.xlsx", engine='xlsxwriter')