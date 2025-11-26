# run_scanner.py
import schedule
import time
from src.data_fetcher import OddsFetcher
from src.arbitrage_finder import ArbitrageFinder
from src.database import OddsDatabase

def scan_for_arbitrage():
    fetcher = OddsFetcher('your_api_key')
    finder = ArbitrageFinder(min_profit_percent=0.5)
    db = OddsDatabase()
    
    # Fetch odds
    odds_df = fetcher.get_odds('basketball_nba')
    db.insert_odds(odds_df)
    
    # Find arbitrage
    arbs = finder.find_arbitrage_two_way(odds_df)
    
    # Store opportunities
    for arb in arbs:
        db.insert_arbitrage(arb)
        print(f"Found: {arb['home_team']} vs {arb['away_team']} - {arb['profit_percent']}%")

# Run every 5 minutes
schedule.every(5).minutes.do(scan_for_arbitrage)

print("Arbitrage scanner started...")
while True:
    schedule.run_pending()
    time.sleep(1)