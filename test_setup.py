import requests
import os

API_KEY = 'e635c57ec280e254cc305863ad085c27'
SPORT = 'basketball_nba'  # or 'americanfootball_nfl', 'baseball_mlb'
REGIONS = 'us'  # US bookmakers
MARKETS = 'h2h'  # head-to-head (moneyline)

url = f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds'
params = {
    'apiKey': API_KEY,
    'regions': REGIONS,
    'markets': MARKETS,
    'oddsFormat': 'decimal'
}

response = requests.get(url, params=params)
print(response.json())