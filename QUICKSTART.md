# Quick Start Guide - Market Data Analyzer

## Installation (30 seconds)

```bash
# Install Python dependencies
pip install -r requirements.txt

# Optional: Build OCaml module
cd ocaml_analytics && ./build.sh && cd ..
```

## Quick Commands

### 1. Run Comprehensive Demo
```bash
python3 demo.py
```
Shows all features without plots - perfect for quick testing!

### 2. Basic Analysis
```bash
python3 main.py --symbol AAPL
```
Generates data and shows price charts for a single stock.

### 3. Compare Multiple Stocks
```bash
python3 main.py --symbols AAPL GOOGL MSFT TSLA --days 180
```
Compare performance of multiple stocks.

### 4. Create Dashboard
```bash
python3 main.py --symbol NVDA --dashboard
```
Comprehensive multi-panel dashboard with all analytics.

### 5. Analytics Only (No Charts)
```bash
python3 main.py --symbol TSLA --no-plot
```
Just show the numbers, skip visualization.

### 6. With OCaml Analytics
```bash
python3 main.py --symbol MSFT --use-ocaml
```
Compare Python vs OCaml implementations.

### 7. Save Results
```bash
python3 main.py --symbol AAPL --save-csv data.csv --save-plot chart.png
```
Export data and visualizations to files.

## Individual Module Testing

### Test Data Fetcher
```bash
python3 src/data_fetcher.py
```

### Test Analytics
```bash
python3 src/analytics.py
```

### Test Visualizer
```bash
python3 src/visualizer.py
```

### Test OCaml Module
```bash
cd ocaml_analytics
./analytics.exe
```

## Python Module Usage

```python
# Import modules
from src.data_fetcher import MarketDataFetcher
from src.analytics import MarketAnalytics
from src.visualizer import MarketVisualizer

# Generate data
fetcher = MarketDataFetcher()
df = fetcher.generate_stock_prices("AAPL", days=252)

# Compute analytics
analytics = MarketAnalytics()
report = analytics.generate_summary_report(df, "AAPL")
print(report)

# Visualize
viz = MarketVisualizer()
viz.plot_price_history(df, "AAPL")
viz.create_dashboard(df, "AAPL")
```

## Key Metrics Explained

- **Mean Price**: Average closing price over the period
- **Volatility**: Standard deviation of returns (measure of risk)
  - Daily: Day-to-day price fluctuations
  - Annual: Annualized volatility (daily × √252)
- **Sharpe Ratio**: Risk-adjusted return (higher is better)
  - > 1.0 = Good, > 2.0 = Very good, > 3.0 = Excellent
- **Max Drawdown**: Largest peak-to-trough decline
- **Total Return**: Overall percentage change from start to end
- **RSI**: Relative Strength Index (0-100)
  - > 70 = Overbought, < 30 = Oversold

## Customization Examples

### Custom Time Period
```bash
python3 main.py --symbol AAPL --days 500
```

### Different Moving Average Windows
```python
viz.plot_moving_averages(df, ma_windows=[10, 20, 50, 200])
```

### Custom Bollinger Bands
```python
viz.plot_bollinger_bands(df, window=20, num_std=3.0)
```

## Troubleshooting

### Issue: "No module named 'matplotlib'"
```bash
pip install -r requirements.txt
```

### Issue: OCaml not building
```bash
# Install OCaml
sudo apt-get install ocaml

# Rebuild
cd ocaml_analytics && ./build.sh
```

### Issue: Plots not showing
- Add `save_path` parameter to save to file
- Or use `--no-plot` flag to skip visualization

## Advanced Usage

### Generate and Save Multiple Stocks
```python
fetcher = MarketDataFetcher()
stocks = fetcher.generate_multiple_stocks(
    ["AAPL", "GOOGL", "MSFT"], 
    days=365
)

for symbol, df in stocks.items():
    fetcher.save_to_csv(df, f"{symbol}_data.csv")
```

### Custom Analytics
```python
# Compute custom metrics
returns = analytics.compute_returns(df)
vol_20 = analytics.compute_volatility(returns.rolling(20))
rsi = analytics.compute_rsi(df, window=14)
```

### Multi-Stock Dashboard
```python
stocks = fetcher.generate_multiple_stocks(["AAPL", "GOOGL", "MSFT"])
viz.plot_multiple_stocks(stocks, normalize=True)
```

## What's Next?

- Try different symbols and time periods
- Experiment with technical indicators
- Compare Python vs OCaml performance
- Add your own analytics functions
- Integrate real market data APIs

Enjoy analyzing! 📈
