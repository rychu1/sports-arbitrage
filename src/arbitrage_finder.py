import pandas as pd
import numpy as np
from itertools import combinations

class ArbitrageFinder:
    def __init__(self, min_profit_percent=0.5):
        """
        min_profit_percent: minimum profit % to flag as arbitrage
        (account for bookmaker limits, fees, etc.)
        """
        self.min_profit_percent = min_profit_percent
    
    def american_to_decimal(self, american_odds):
        """Convert American odds to decimal"""
        if american_odds > 0:
            return (american_odds / 100) + 1
        else:
            return (100 / abs(american_odds)) + 1
    
    def calculate_implied_probability(self, decimal_odds):
        """Calculate implied probability from decimal odds"""
        return 1 / decimal_odds
    
    def find_arbitrage_two_way(self, odds_df):
        """
        Find arbitrage opportunities for two-way markets (moneyline)
        
        Input: DataFrame with columns [game_id, team, bookmaker, odds]
        Output: List of arbitrage opportunities
        """
        opportunities = []
        
        # Group by game
        for game_id, game_data in odds_df.groupby('game_id'):
            home_team = game_data['home_team'].iloc[0]
            away_team = game_data['away_team'].iloc[0]
            
            # Get all odds for home team
            home_odds = game_data[game_data['team'] == home_team]
            # Get all odds for away team
            away_odds = game_data[game_data['team'] == away_team]
            
            # Try all combinations of bookmakers
            for _, home_row in home_odds.iterrows():
                for _, away_row in away_odds.iterrows():
                    
                    # Skip same bookmaker (can't arb with yourself)
                    if home_row['bookmaker'] == away_row['bookmaker']:
                        continue
                    
                    home_decimal = home_row['odds']
                    away_decimal = away_row['odds']
                    
                    # Calculate arbitrage
                    arb_percentage = (1/home_decimal + 1/away_decimal) * 100
                    profit_percent = 100 - arb_percentage
                    
                    if profit_percent >= self.min_profit_percent:
                        # Calculate optimal bet allocation
                        total_stake = 1000  # Example: $1000 total
                        stake_home = total_stake * (1/home_decimal) / (1/home_decimal + 1/away_decimal)
                        stake_away = total_stake - stake_home
                        
                        # Calculate guaranteed returns
                        return_home = stake_home * home_decimal
                        return_away = stake_away * away_decimal
                        guaranteed_profit = min(return_home, return_away) - total_stake
                        
                        opportunities.append({
                            'game_id': game_id,
                            'home_team': home_team,
                            'away_team': away_team,
                            'bookmaker_home': home_row['bookmaker'],
                            'bookmaker_away': away_row['bookmaker'],
                            'odds_home': home_decimal,
                            'odds_away': away_decimal,
                            'profit_percent': round(profit_percent, 2),
                            'stake_home': round(stake_home, 2),
                            'stake_away': round(stake_away, 2),
                            'guaranteed_profit': round(guaranteed_profit, 2),
                            'commence_time': home_row['commence_time']
                        })
        
        return sorted(opportunities, key=lambda x: x['profit_percent'], reverse=True)
    
    def find_arbitrage_three_way(self, odds_df):
        """
        For sports with draws (soccer, hockey)
        Similar logic but with 3 outcomes
        """
        # Implementation for 3-way markets
        pass  # You can expand this later

# Usage example
if __name__ == '__main__':
    from data_fetcher import OddsFetcher
    
    fetcher = OddsFetcher('your_api_key')
    odds_df = fetcher.get_odds('basketball_nba')
    
    finder = ArbitrageFinder(min_profit_percent=0.5)
    arbs = finder.find_arbitrage_two_way(odds_df)
    
    print(f"Found {len(arbs)} arbitrage opportunities!")
    for arb in arbs[:5]:  # Show top 5
        print(f"\n{arb['home_team']} vs {arb['away_team']}")
        print(f"Profit: {arb['profit_percent']}%")
        print(f"Bet ${arb['stake_home']:.2f} on {arb['home_team']} at {arb['bookmaker_home']}")
        print(f"Bet ${arb['stake_away']:.2f} on {arb['away_team']} at {arb['bookmaker_away']}")
        print(f"Guaranteed profit: ${arb['guaranteed_profit']:.2f}")