import sqlite3
import pandas as pd
from datetime import datetime
import tempfile
import os

class OddsDatabase:
    def __init__(self, db_path=None):
        # Streamlit Cloud has read-only filesystem except temp directory
        if db_path is None:
            # Check if running on Streamlit Cloud
            if os.path.exists('/mount/src'):  # Streamlit Cloud indicator
                # Use temp directory on cloud
                self.db_path = os.path.join(tempfile.gettempdir(), 'odds_history.db')
                print(f"Running on Streamlit Cloud. Database at: {self.db_path}")
            else:
                # Running locally - use data folder
                self.db_path = 'data/odds_history.db'
                os.makedirs('data', exist_ok=True)
                print(f"Running locally. Database at: {self.db_path}")
        else:
            self.db_path = db_path
        
        self.create_tables()
    
    def create_tables(self):
        """Initialize database schema"""
        try:
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
            print(f"✅ Database initialized successfully at {self.db_path}")
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            raise
    
    def insert_odds(self, df):
        """Store odds data"""
        try:
            conn = sqlite3.connect(self.db_path)
            df.to_sql('odds', conn, if_exists='append', index=False)
            conn.close()
            print(f"✅ Inserted {len(df)} odds records")
        except Exception as e:
            print(f"❌ Error inserting odds: {e}")
    
    def insert_arbitrage(self, arb_data):
        """Store detected arbitrage opportunities"""
        try:
            conn = sqlite3.connect(self.db_path)
            pd.DataFrame([arb_data]).to_sql(
                'arbitrage_opportunities', 
                conn, 
                if_exists='append', 
                index=False
            )
            conn.close()
            print(f"✅ Inserted arbitrage opportunity")
        except Exception as e:
            print(f"❌ Error inserting arbitrage: {e}")
    
    def get_latest_odds(self, game_id=None):
        """Retrieve most recent odds"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            if game_id:
                query = f"SELECT * FROM odds WHERE game_id = '{game_id}' ORDER BY timestamp DESC"
            else:
                query = "SELECT * FROM odds ORDER BY timestamp DESC LIMIT 1000"
            
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df
        except Exception as e:
            print(f"❌ Error getting odds: {e}")
            return pd.DataFrame()
    
    def get_arbitrage_history(self, days=7):
        """Get historical arbitrage opportunities"""
        try:
            conn = sqlite3.connect(self.db_path)
            query = f"""
                SELECT * FROM arbitrage_opportunities 
                WHERE timestamp >= datetime('now', '-{days} days')
                ORDER BY profit_percent DESC
            """
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df
        except Exception as e:
            print(f"❌ Error getting arbitrage history: {e}")
            return pd.DataFrame()