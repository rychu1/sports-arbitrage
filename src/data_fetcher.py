import requests
import pandas as pd
from datetime import datetime
import time

class OddsFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.the-odds-api.com/v4'
        
    def get_sports(self):
        """Get list of available sports"""
        url = f'{self.base_url}/sports'
        params = {'apiKey': self.api_key}
        response = requests.get(url, params=params)
        return response.json()
    
    def get_odds(self, sport='basketball_nba', markets='h2h'):
        """Fetch current odds for a sport"""
        url = f'{self.base_url}/sports/{sport}/odds'
        params = {
            'apiKey': self.api_key,
            'regions': 'us',
            'markets': markets,
            'oddsFormat': 'decimal'
        }
        
        response = requests.get(url, params=params)
        
        # Check remaining quota
        remaining = response.headers.get('x-requests-remaining')
        print(f"Requests remaining: {remaining}")
        
        if response.status_code == 200:
            return self.parse_odds_data(response.json())
        else:
            print(f"Error: {response.status_code}")
            return None
    
    def parse_odds_data(self, raw_data):
        """Convert API response to structured DataFrame"""
        parsed_games = []
        
        for game in raw_data:
            game_id = game['id']
            home_team = game['home_team']
            away_team = game['away_team']
            commence_time = game['commence_time']
            
            # Extract odds from each bookmaker
            for bookmaker in game['bookmakers']:
                bookmaker_name = bookmaker['title']
                
                for market in bookmaker['markets']:
                    if market['key'] == 'h2h':
                        for outcome in market['outcomes']:
                            parsed_games.append({
                                'game_id': game_id,
                                'home_team': home_team,
                                'away_team': away_team,
                                'commence_time': commence_time,
                                'bookmaker': bookmaker_name,
                                'team': outcome['name'],
                                'odds': outcome['price'],
                                'timestamp': datetime.now()
                            })
        
        return pd.DataFrame(parsed_games)

# Usage example
if __name__ == '__main__':
    fetcher = OddsFetcher('your_api_key')
    df = fetcher.get_odds('basketball_nba')
    print(df.head())
    print(f"\nShape: {df.shape}")