# 🌐 Market Data Analyzer - Web Application Guide

## Quick Start

### Starting the Server

```bash
# Start the web server
python3 web_app.py

# Or use the Makefile
make web
```

The application will be available at: **http://localhost:5000**

---

## Features Overview

### 🎯 Single Stock Analysis

**What it does**: Analyzes a single stock with comprehensive metrics and visualizations

**How to use:**
1. Enter a stock symbol (e.g., AAPL, GOOGL, MSFT)
2. Choose analysis period (30-365 days)
3. ✅ Check "Use Real Market Data" for live Yahoo Finance data
4. Click "Generate Analysis"

**What you get:**
- 📊 6 Professional Charts:
  - Price history with volume
  - Returns distribution
  - Moving averages (20 & 50 day)
  - Bollinger Bands
  - Volatility analysis (30-day rolling)
  - Comprehensive dashboard

- 📈 Key Metrics:
  - Mean price
  - Annual volatility
  - Sharpe ratio
  - Total return
  - Maximum drawdown
  - Price range

---

### 🔄 Multi-Stock Comparison

**What it does**: Compares multiple stocks side-by-side with normalized prices

**How to use:**
1. Enter comma-separated symbols (e.g., AAPL,GOOGL,MSFT)
2. Choose comparison period
3. ✅ Check "Use Real Market Data" for live data
4. Click "Compare Stocks"

**What you get:**
- 📊 Normalized price comparison chart
- 📊 Performance metrics for each stock:
  - Mean price
  - Returns
  - Sharpe ratio
  - Volatility
  - Data source indicator

---

## 🔍 Data Sources

### Real Market Data (Yahoo Finance)
- ✅ **Live data** from Yahoo Finance API
- Updates daily with actual market prices
- Historical OHLC (Open, High, Low, Close) data
- Actual trading volume
- Perfect for real analysis

**Enable by**: Checking the "Use Real Market Data" box

### Simulated Data (GBM)
- ⚡ **Instant generation** using Geometric Brownian Motion
- Statistical properties similar to real markets
- Configurable volatility and drift
- Perfect for testing and demos

**Enable by**: Unchecking the "Use Real Market Data" box

---

## 💡 Tips & Best Practices

### Choosing Symbols
- Use standard ticker symbols (uppercase)
- Examples: AAPL, GOOGL, MSFT, TSLA, AMZN, META
- For ETFs: SPY, QQQ, VOO
- Invalid symbols automatically fall back to simulated data

### Time Periods
- **Short-term (30-90 days)**: Recent trends, daily volatility
- **Medium-term (90-180 days)**: Quarterly performance
- **Long-term (180-365 days)**: Annual analysis, seasonality

### Real vs Simulated
- **Use Real Data** when:
  - Analyzing actual market conditions
  - Preparing investment research
  - Comparing historical performance
  
- **Use Simulated Data** when:
  - Testing the system
  - Demonstrating features
  - Real data is unavailable

---

## 🎨 Understanding the Interface

### Data Source Badges
- 🟢 **"✓ Real Data"** (Green): Using Yahoo Finance data
- 🟡 **"⚡ Simulated"** (Yellow): Using GBM simulation

### Metric Cards
Each metric card shows:
- **Large number**: The calculated value
- **Label**: What the metric represents
- **Color-coded**: Different colors for different types

### Charts
All charts include:
- ✅ Professional styling with seaborn
- ✅ Clear labels and legends
- ✅ High-resolution output
- ✅ Downloadable PNG files

---

## 🔧 Technical Details

### API Endpoints

#### POST /generate
Generates analysis for a single stock.

**Request:**
```json
{
  "symbol": "AAPL",
  "days": 90,
  "use_real_data": true
}
```

**Response:**
```json
{
  "success": true,
  "symbol": "AAPL",
  "data_source": "Real Market Data (Yahoo Finance)",
  "days": 90,
  "date_range": "2025-07-08 to 2025-11-11",
  "report": {
    "mean_price": "$238.01",
    "volatility_annual": "23.46%",
    "sharpe_ratio": "3.326",
    "max_drawdown": "-5.61%",
    "total_return": "31.34%",
    "min_price": "$201.95",
    "max_price": "$275.25"
  },
  "visualizations": {
    "price": "/static/images/price_AAPL_*.png",
    "returns": "/static/images/returns_AAPL_*.png",
    "ma": "/static/images/ma_AAPL_*.png",
    "bollinger": "/static/images/bollinger_AAPL_*.png",
    "volatility": "/static/images/volatility_AAPL_*.png",
    "dashboard": "/static/images/dashboard_AAPL_*.png"
  }
}
```

#### POST /compare
Compares multiple stocks.

**Request:**
```json
{
  "symbols": "AAPL,GOOGL,MSFT",
  "days": 90,
  "use_real_data": true
}
```

**Response:**
```json
{
  "success": true,
  "symbols": ["AAPL", "GOOGL", "MSFT"],
  "reports": {
    "AAPL": {
      "data_source": "Real",
      "mean_price": "$238.01",
      "return": "31.34%",
      "sharpe": "3.326",
      "volatility": "23.46%"
    },
    "GOOGL": {...},
    "MSFT": {...}
  },
  "visualization": "/static/images/comparison_*.png"
}
```

---

## 🐛 Troubleshooting

### Server Won't Start
```bash
# Check if port 5000 is already in use
lsof -i :5000

# Kill existing process
pkill -f web_app.py

# Restart
python3 web_app.py
```

### No Real Data Available
- **Symptom**: Getting simulated data when requesting real data
- **Causes**:
  - Invalid stock symbol
  - Network issues
  - Yahoo Finance API temporary unavailable
- **Solution**: System automatically falls back to simulated data

### Charts Not Loading
- **Check**: `/static/images/` directory exists
- **Check**: Matplotlib backend is configured
- **Check**: Write permissions on directory

### Slow Performance
- **Real data fetching**: Takes 4-6 seconds per request (normal)
- **Multiple stocks**: Each stock requires separate API call
- **Solution**: Use simulated data for faster testing

---

## 📊 Example Use Cases

### 1. Daily Portfolio Check
```
Symbols: AAPL,MSFT,GOOGL
Days: 30
Real Data: ✅ Checked
```
→ Compare your holdings over the last month

### 2. Quarterly Performance Review
```
Symbol: SPY
Days: 90
Real Data: ✅ Checked
```
→ Analyze S&P 500 quarterly performance

### 3. Demo for Presentation
```
Symbol: TSLA
Days: 180
Real Data: ❌ Unchecked
```
→ Instant simulated data for demonstration

### 4. Algorithm Testing
```
Symbols: Multiple tech stocks
Days: 365
Real Data: ❌ Unchecked
```
→ Test analytics with consistent simulated data

---

## 🔒 Limitations

1. **Data Frequency**: Yahoo Finance provides daily data only (no intraday)
2. **Historical Limit**: Typically limited to several years of history
3. **Rate Limits**: Excessive requests may be throttled
4. **Market Hours**: Real data reflects market close prices
5. **Delisted Stocks**: Historical data may be incomplete

---

## 🚀 Advanced Features

### Customization
The web interface can be extended by modifying:
- `web_app.py`: Backend logic and routes
- `templates/index.html`: UI and styling
- `src/analytics.py`: Add new metrics
- `src/visualizer.py`: Add new chart types

### Integration
Use the API endpoints to integrate with:
- Jupyter notebooks
- Automated trading systems
- Portfolio management tools
- Research platforms

---

## 📚 Related Documentation

- **[QUICKSTART.md](QUICKSTART.md)**: Command-line usage
- **[README.md](README.md)**: Project overview
- **[TESTING_REPORT.md](TESTING_REPORT.md)**: Test results
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)**: Technical details

---

## 🤝 Support

For issues or questions:
1. Check the logs: `web_app.log`
2. Review error messages in browser console
3. Verify dependencies are installed: `pip install -r requirements.txt`
4. Ensure OCaml module is compiled: `make build-ocaml`

---

**Happy Analyzing! 📈**
