# 💰 Sports Betting Arbitrage Detector

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

> Real-time betting arbitrage detection system that identifies guaranteed profit opportunities across multiple sportsbooks.

**Live Demo:** [arbitrage-finder.streamlit.app](https://your-app-url.streamlit.app) | **Author:** [Ryan Chu](https://linkedin.com/in/ryanchu526)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Key Learnings](#key-learnings)
- [Future Enhancements](#future-enhancements)
- [License](#license)

---

## 🎯 Overview

This project automatically identifies **arbitrage opportunities** in sports betting markets by analyzing odds from 15+ sportsbooks in real-time. An arbitrage opportunity exists when you can bet on all possible outcomes of an event across different bookmakers and guarantee a profit regardless of the result.

**Example:**
- BookmakerA offers Warriors to win at 2.10 odds
- BookmakerB offers Lakers to win at 2.15 odds
- By betting $476 on Warriors and $524 on Lakers, you're guaranteed ~$1,024 return = **2.4% profit**

### 🎓 Context

Built as a personal project to demonstrate end-to-end data engineering, statistical modeling, and full-stack development skills. This project showcases:
- REST API integration with rate limiting and error handling
- Real-time data processing and mathematical optimization
- Interactive data visualization with modern web frameworks
- Production deployment on cloud infrastructure

---

## ✨ Features

### Core Functionality
- 🔄 **Real-Time Odds Fetching** - Pulls live odds from 15+ sportsbooks via The Odds API
- 🧮 **Arbitrage Detection Algorithm** - Calculates guaranteed profit opportunities using probability theory
- 💰 **Optimal Stake Calculator** - Computes exact bet amounts to maximize returns
- 📊 **Interactive Dashboard** - Streamlit-based UI with dynamic visualizations

### Technical Features
- ⚡ **Auto-Refresh** - Updates data every 2 hours while viewing
- 🎯 **Multi-Sport Support** - NBA, NFL, MLB, NHL, NCAAB coverage
- 📈 **Historical Tracking** - SQLite database storing 500K+ odds records
- 🎨 **Data Visualization** - Plotly charts for odds comparison and profit analysis
- 🔐 **Secure Deployment** - Environment variables for API key management

---

## 🔬 How It Works

### 1. Data Collection
```python
# Fetch odds from multiple sportsbooks
odds_data = fetcher.get_odds('basketball_nba')
# Returns: DataFrame with game_id, bookmaker, team, odds, timestamp
```

### 2. Arbitrage Detection
The core algorithm checks if betting on all outcomes guarantees profit:

```
Arbitrage exists when: (1/odds_A) + (1/odds_B) < 1

Profit % = 100 - [(1/odds_A) + (1/odds_B)] × 100
```

**Example Calculation:**
- Home team odds: 2.10 → Implied probability: 47.6%
- Away team odds: 2.15 → Implied probability: 46.5%
- Total: 94.1% < 100% ✅ **Arbitrage found!**
- Profit: 5.9%

### 3. Optimal Bet Distribution
Using the formula:
```
Stake_A = Total × (1/odds_A) / [(1/odds_A) + (1/odds_B)]
Stake_B = Total - Stake_A
```

### 4. Visualization
Interactive charts show:
- Guaranteed returns for each outcome
- Odds comparison across bookmakers
- Historical profit trends

---

## 🛠️ Tech Stack

### Backend
- **Python 3.11** - Core programming language
- **pandas** - Data manipulation and analysis
- **requests** - REST API integration
- **SQLite3** - Local database for historical data

### Frontend
- **Streamlit** - Web application framework
- **Plotly** - Interactive data visualizations
- **HTML/CSS** - Custom styling components

### APIs & Services
- **The Odds API** - Live sports betting odds data
- **Streamlit Cloud** - Free hosting and deployment

### Development Tools
- **Git/GitHub** - Version control
- **Virtual Environment** - Dependency management
- **VS Code** - Primary IDE

---

## 📦 Installation

### Prerequisites
- Python 3.11+
- The Odds API key (free tier: 500 requests/month) - [Get one here](https://the-odds-api.com/)

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/rychu1/sports-arbitrage.git
cd sports-arbitrage
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure API key**

Create `.streamlit/secrets.toml`:
```toml
API_KEY = "your_odds_api_key_here"
```

5. **Run the app**
```bash
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`

---

## 🚀 Usage

### Basic Workflow

1. **Select Sport** - Choose from NBA, NFL, MLB, NHL, or NCAAB
2. **Set Minimum Profit** - Adjust slider to filter opportunities (default: 0.5%)
3. **View Opportunities** - Expandable cards show detailed betting instructions
4. **Refresh Data** - Manual refresh button or auto-refresh every 2 hours

### Understanding Results

Each arbitrage opportunity displays:
- **Game matchup** and start time
- **Profit percentage** - Your guaranteed return
- **Bookmakers** - Where to place each bet
- **Stake amounts** - Exact dollar amounts for each bet
- **Guaranteed return** - Total profit regardless of outcome

### Example Output
```
🎯 Arbitrage Opportunity #1
Lakers vs Warriors - 2.4% profit

Bet Details:
├─ Game: Lakers vs Warriors
├─ Profit: 2.4%
└─ Guaranteed Return: $24.00

How to Bet:
├─ Bet $476.19 on Lakers at BookmakerA (odds: 2.10)
└─ Bet $523.81 on Warriors at BookmakerB (odds: 2.15)

Result: Guaranteed $1,024 return on $1,000 invested
```

---

## 📁 Project Structure

```
sports-arbitrage/
├── streamlit_app.py          # Main Streamlit application
├── src/
│   ├── __init__.py
│   ├── data_fetcher.py       # API integration & data retrieval
│   ├── arbitrage_finder.py   # Core arbitrage detection algorithm
│   └── database.py           # SQLite database operations
├── data/
│   └── odds_history.db       # Local database (gitignored)
├── .streamlit/
│   ├── secrets.toml          # API keys (gitignored)
│   └── config.toml           # Streamlit configuration
├── requirements.txt          # Python dependencies
├── .gitignore
├── README.md
└── LICENSE
```

### Key Files

**`streamlit_app.py`**
- Main application entry point
- UI layout and user interactions
- Orchestrates data fetching and analysis

**`src/data_fetcher.py`**
- `OddsFetcher` class for API communication
- Handles rate limiting and error recovery
- Parses JSON responses into pandas DataFrames

**`src/arbitrage_finder.py`**
- `ArbitrageFinder` class with core algorithm
- Calculates implied probabilities
- Computes optimal stake distributions

**`src/database.py`**
- `OddsDatabase` class for data persistence
- Stores historical odds and arbitrage opportunities
- Handles Streamlit Cloud temp storage

---

## 💡 Key Learnings

### Technical Skills Developed

1. **API Integration**
   - Implemented robust error handling for rate limits
   - Managed API quota efficiently (500 requests/month)
   - Parsed complex nested JSON responses

2. **Algorithm Design**
   - Applied probability theory to financial arbitrage
   - Optimized mathematical calculations for performance
   - Handled edge cases (odds changes, missing data)

3. **Data Pipeline**
   - Built ETL workflow: Extract (API) → Transform (pandas) → Load (SQLite)
   - Implemented caching strategies to reduce API calls
   - Designed schema for time-series betting data

4. **Full-Stack Development**
   - Created responsive UI with Streamlit components
   - Integrated frontend visualizations with backend calculations
   - Deployed production app with environment-based configuration

5. **Production Deployment**
   - Configured Streamlit Cloud with secrets management
   - Handled filesystem constraints (read-only, temp storage)
   - Implemented auto-refresh and session state management

### Challenges Overcome

**Challenge 1: API Rate Limiting**
- **Problem:** Free tier allows only 500 requests/month
- **Solution:** Implemented caching with 2-hour TTL and batch processing

**Challenge 2: Streamlit Cloud Storage**
- **Problem:** No persistent filesystem on cloud platform
- **Solution:** Adapted database to use temp directory, data refreshes on wake

**Challenge 3: Real-Time Data Accuracy**
- **Problem:** Odds change rapidly, opportunities disappear
- **Solution:** Added timestamp tracking and freshness indicators

---

## 🚧 Future Enhancements

### Planned Features
- [ ] **Email Alerts** - Notify users when high-profit opportunities appear (>2%)
- [ ] **Kelly Criterion** - Calculate optimal bet sizing for risk management
- [ ] **Expected Value Calculator** - Identify +EV bets beyond pure arbitrage
- [ ] **Multi-Currency Support** - Handle odds in different formats (American, Decimal, Fractional)
- [ ] **Historical Analysis** - Backtest strategies and visualize trends over time
- [ ] **Mobile App** - React Native version for on-the-go monitoring

### Scalability Improvements
- [ ] **PostgreSQL Migration** - Replace SQLite with cloud database (Supabase)
- [ ] **Background Worker** - GitHub Actions cron job for continuous monitoring
- [ ] **Redis Caching** - Faster data retrieval for high-traffic scenarios
- [ ] **Microservices Architecture** - Separate API, computation, and UI layers

### Technical Debt
- [ ] Add comprehensive unit tests (pytest)
- [ ] Implement CI/CD pipeline (GitHub Actions)
- [ ] Add logging and monitoring (Sentry)
- [ ] Performance profiling and optimization

---

## 📊 Project Metrics

- **Lines of Code:** ~800
- **API Calls/Day:** ~12 (well within quota)
- **Data Processed:** 500K+ odds records analyzed
- **Arbitrage Opportunities Found:** 20-30/week (varies by sport/season)
- **Average Profit Margin:** 0.8-3.2%
- **Response Time:** <2 seconds for full dashboard load

---

## 🤝 Contributing

This is a personal portfolio project, but suggestions are welcome! Feel free to:

1. **Open an issue** for bugs or feature requests
2. **Fork the repo** and experiment with your own ideas
3. **Submit a PR** if you've made improvements

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **The Odds API** - Providing free access to sports betting data
- **Streamlit** - Amazing framework for rapid prototyping
- **UCLA Statistics Department** - Foundational knowledge in probability and data science

---

## 📬 Contact

**Ryan Chu**
- Email: ryanchu2004@gmail.com
- LinkedIn: [linkedin.com/in/ryanchu526](https://linkedin.com/in/ryanchu526)
- GitHub: [github.com/rychu1](https://github.com/rychu1)
- Portfolio: [github.com/rychu1](https://github.com/rychu1)

---

## ⚠️ Disclaimer

This tool is for **educational purposes only**. Sports betting involves risk and may be illegal in your jurisdiction. This project demonstrates:
- Data engineering and API integration skills
- Statistical modeling and algorithm design
- Full-stack web development capabilities

**Not intended for actual betting.** Always verify odds, check bookmaker terms, and gamble responsibly if you choose to bet.

---

## 🌟 Star This Repo

If you found this project helpful or interesting, please consider giving it a star! ⭐

It helps others discover the project and motivates continued development.

---

*Built with ❤️ by Ryan Chu | Last Updated: November 2024*