import sqlite3
import pandas as pd
from datetime import datetime

class OddsDatabase:
    def __init__(self, db_path='data/odds_history.db'):
        self.db_path = db_path
        self.create_tables()
    
    def create_tables(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS odds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id TEXT,
                home_team TEXT,
                away_team TEXT,
                commence_time TEXT,
                bookmaker TEXT,
                team TEXT,
                odds REAL,
                timestamp TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS arbitrage_opportunities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id TEXT,
                home_team TEXT,
                away_team TEXT,
                bookmaker_1 TEXT,
                bookmaker_2 TEXT,
                team_1 TEXT,
                team_2 TEXT,
                odds_1 REAL,
                odds_2 REAL,
                profit_percent REAL,
                timestamp TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def insert_odds(self, df):
        """Store odds data"""
        conn = sqlite3.connect(self.db_path)
        df.to_sql('odds', conn, if_exists='append', index=False)
        conn.close()
    
    def insert_arbitrage(self, arb_data):
        """Store detected arbitrage opportunities"""
        conn = sqlite3.connect(self.db_path)
        pd.DataFrame([arb_data]).to_sql(
            'arbitrage_opportunities', 
            conn, 
            if_exists='append', 
            index=False
        )
        conn.close()
    
    def get_latest_odds(self, game_id=None):
        """Retrieve most recent odds"""
        conn = sqlite3.connect(self.db_path)
        
        if game_id:
            query = f"SELECT * FROM odds WHERE game_id = '{game_id}' ORDER BY timestamp DESC"
        else:
            query = "SELECT * FROM odds ORDER BY timestamp DESC LIMIT 1000"
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def get_arbitrage_history(self, days=7):
        """Get historical arbitrage opportunities"""
        conn = sqlite3.connect(self.db_path)
        query = f"""
            SELECT * FROM arbitrage_opportunities 
            WHERE timestamp >= datetime('now', '-{days} days')
            ORDER BY profit_percent DESC
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df