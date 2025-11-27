import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Sports Arbitrage Detector",
    page_icon="💰",
    layout="wide"
) 

# Clean imports (no sys.path hacks needed)
from src.data_fetcher import OddsFetcher
from src.arbitrage_finder import ArbitrageFinder
from src.database import OddsDatabase

# Initialize
@st.cache_resource
def init_components():
    fetcher = OddsFetcher(st.secrets["API_KEY"])
    finder = ArbitrageFinder(min_profit_percent=0.3)
    db = OddsDatabase()
    return fetcher, finder, db

fetcher, finder, db = init_components()

# Sidebar
st.sidebar.title("⚙️ Settings")
sport = st.sidebar.selectbox(
    "Select Sport",
    ["basketball_nba", "basketball_ncaab", "americanfootball_nfl", "baseball_mlb", "icehockey_nhl"]
)

min_profit = st.sidebar.slider("Minimum Profit %", 0.0, 5.0, 0.5, 0.1)
finder.min_profit_percent = min_profit

refresh = st.sidebar.button("🔄 Refresh Data")

# Main content
st.title("💰 Sports Betting Arbitrage Detector")
st.markdown("Find guaranteed profit opportunities across sportsbooks")

# Fetch data
if refresh or 'odds_df' not in st.session_state:
    with st.spinner("Fetching latest odds..."):
        st.session_state.odds_df = fetcher.get_odds(sport)
        db.insert_odds(st.session_state.odds_df)

odds_df = st.session_state.odds_df

# Find arbitrage
arb_opportunities = finder.find_arbitrage_two_way(odds_df)

# Display metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Games Analyzed", odds_df['game_id'].nunique())
with col2:
    st.metric("Bookmakers", odds_df['bookmaker'].nunique())
with col3:
    st.metric("Arb Opportunities", len(arb_opportunities))
with col4:
    if arb_opportunities:
        best_profit = arb_opportunities[0]['profit_percent']
        st.metric("Best Profit %", f"{best_profit}%")
    else:
        st.metric("Best Profit %", "0%")

st.markdown("---")

# Display opportunities
if arb_opportunities:
    st.subheader("🎯 Active Arbitrage Opportunities")
    
    for i, arb in enumerate(arb_opportunities):
        with st.expander(
            f"#{i+1}: {arb['home_team']} vs {arb['away_team']} - {arb['profit_percent']}% profit",
            expanded=(i < 3)
        ):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📊 Bet Details")
                st.write(f"**Game:** {arb['home_team']} vs {arb['away_team']}")
                st.write(f"**Commence Time:** {arb['commence_time']}")
                st.write(f"**Profit:** {arb['profit_percent']}%")
                st.write(f"**Guaranteed Return:** ${arb['guaranteed_profit']:.2f}")
            
            with col2:
                st.markdown("### 💵 How to Bet")
                st.success(
                    f"Bet **${arb['stake_home']:.2f}** on **{arb['home_team']}**\n\n"
                    f"at **{arb['bookmaker_home']}** (odds: {arb['odds_home']:.2f})"
                )
                st.info(
                    f"Bet **${arb['stake_away']:.2f}** on **{arb['away_team']}**\n\n"
                    f"at **{arb['bookmaker_away']}** (odds: {arb['odds_away']:.2f})"
                )
            
            # Visualization
            profit_data = pd.DataFrame({
                'Outcome': [arb['home_team'], arb['away_team']],
                'Return': [
                    arb['stake_home'] * arb['odds_home'],
                    arb['stake_away'] * arb['odds_away']
                ]
            })
            
            fig = px.bar(
                profit_data,
                x='Outcome',
                y='Return',
                title="Guaranteed Return by Outcome",
                color='Return',
                color_continuous_scale='Greens'
            )
            fig.add_hline(
                y=1000,
                line_dash="dash",
                annotation_text="Initial Investment",
                annotation_position="right"
            )
            st.plotly_chart(fig, use_container_width=True, key=f"arb_chart_{i}")

else:
    st.warning("No arbitrage opportunities found at current settings. Try lowering the minimum profit percentage.")

# Historical performance
st.markdown("---")
st.subheader("📈 Historical Performance")

hist_arbs = db.get_arbitrage_history(days=30)
if not hist_arbs.empty:
    fig = px.line(
        hist_arbs,
        x='timestamp',
        y='profit_percent',
        title="Arbitrage Profit % Over Time"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(
        hist_arbs[['home_team', 'away_team', 'profit_percent', 'timestamp']].head(20),
        use_container_width=True
    )
else:
    st.info("No historical data yet. Keep the system running to build history!")

# Odds comparison
st.markdown("---")
st.subheader("🔍 Odds Comparison")

selected_game = st.selectbox(
    "Select a game",
    odds_df['game_id'].unique()
)

game_odds = odds_df[odds_df['game_id'] == selected_game]

fig = px.bar(
    game_odds,
    x='bookmaker',
    y='odds',
    color='team',
    barmode='group',
    title=f"Odds Comparison: {game_odds['home_team'].iloc[0]} vs {game_odds['away_team'].iloc[0]}"
)
st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.caption("⚠️ Disclaimer: This tool is for educational purposes. Always verify odds and check bookmaker terms before placing bets.")
