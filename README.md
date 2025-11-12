# Market Data Analyzer

A functional prototype for analyzing market data using **Python** and **OCaml**. This project demonstrates a hybrid approach combining Python's data science ecosystem with OCaml's functional programming capabilities.

## Features

### Python Modules
- **Data Fetcher**: Generate realistic synthetic stock market data using Geometric Brownian Motion
- **Analytics**: Compute comprehensive market statistics including:
  - Mean prices and returns
  - Volatility (daily and annualized)
  - Sharpe ratio
  - Maximum drawdown
  - RSI (Relative Strength Index)
  - Bollinger Bands
- **Visualizer**: Create professional charts and dashboards:
  - Price history with OHLC data
  - Returns distribution
  - Moving averages
  - Bollinger Bands
  - Rolling volatility
  - Multi-stock comparison
  - Comprehensive dashboards

### OCaml Module
- Functional implementation of core analytics:
  - Mean and variance calculations
  - Volatility computation
  - Returns analysis
  - Sharpe ratio
  - Maximum drawdown
- Demonstrates functional programming approach to financial analytics

## Project Structure

```
Market-data-analyzer/
├── main.py                    # Main application entry point
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── src/
│   ├── data_fetcher.py       # Market data generation module
│   ├── analytics.py          # Python analytics module
│   └── visualizer.py         # Visualization module
└── ocaml_analytics/
    ├── analytics.ml          # OCaml analytics implementation
    ├── dune                  # Dune build configuration
    ├── dune-project          # Dune project file
    └── build.sh              # Build script for OCaml module
```

## Installation

### Prerequisites

**Python 3.8+** is required. Install Python dependencies:

```bash
pip install -r requirements.txt
```

**OCaml (Optional)**: For using the OCaml analytics module:

```bash
# On Ubuntu/Debian
sudo apt-get install ocaml opam

# Using opam
opam init
opam install dune
```

### Build OCaml Module (Optional)

```bash
cd ocaml_analytics
./build.sh
```

This creates `analytics.exe` binary that can be called from Python.

## Usage

### Basic Usage

Analyze a single stock with default parameters:

```bash
python main.py --symbol AAPL
```

### Analyze Multiple Stocks

Compare multiple stocks:

```bash
python main.py --symbols AAPL GOOGL MSFT TSLA --days 180
```

### Generate Comprehensive Dashboard

Create a multi-panel dashboard:

```bash
python main.py --symbol NVDA --dashboard
```

### Custom Time Period

Specify number of trading days:

```bash
python main.py --symbol TSLA --days 500
```

### Save Outputs

Save data and plots to files:

```bash
python main.py --symbol AAPL --save-csv data.csv --save-plot chart.png
```

### Use OCaml Analytics

Compute analytics using the OCaml module:

```bash
python main.py --symbol MSFT --use-ocaml
```

### Command Line Options

```
usage: main.py [-h] [--symbol SYMBOL] [--symbols SYMBOLS [SYMBOLS ...]]
               [--days DAYS] [--dashboard] [--save-csv SAVE_CSV]
               [--save-plot SAVE_PLOT] [--no-plot] [--use-ocaml]

Options:
  --symbol SYMBOL              Single stock symbol to analyze (default: STOCK)
  --symbols SYMBOLS [...]      Multiple stock symbols to compare
  --days DAYS                  Number of trading days (default: 252)
  --dashboard                  Create comprehensive dashboard
  --save-csv SAVE_CSV          Save data to CSV file
  --save-plot SAVE_PLOT        Save plot to file
  --no-plot                    Skip plotting (only show analytics)
  --use-ocaml                  Use OCaml module for analytics
```

## Using Individual Modules

### Data Fetcher

```python
from src.data_fetcher import MarketDataFetcher

fetcher = MarketDataFetcher()
df = fetcher.generate_stock_prices("AAPL", days=252)
print(df.head())
```

### Analytics

```python
from src.analytics import MarketAnalytics

analytics = MarketAnalytics()
report = analytics.generate_summary_report(df, "AAPL")
print(report)
```

### Visualizer

```python
from src.visualizer import MarketVisualizer

viz = MarketVisualizer()
viz.plot_price_history(df, "AAPL")
viz.create_dashboard(df, "AAPL")
```

### OCaml Module (Standalone)

```bash
cd ocaml_analytics
./analytics.exe
```

Or with a JSON file containing prices:

```bash
echo '[100.0, 102.5, 101.8, 104.2, 103.5]' > prices.json
./analytics.exe prices.json
```

## Example Output

```
============================================================
Market Data Analyzer
============================================================

Generating data for AAPL...
Period: 252 trading days

Generated 252 data points
Date range: 2024-11-13 to 2025-11-12

============================================================
Analytics Report
============================================================
  symbol........................ AAPL
  period........................ 2024-11-13 to 2025-11-12
  total_days.................... 252
  mean_price.................... 103.5421
  mean_daily_return............. 0.0002
  volatility_daily.............. 0.0195
  volatility_annual............. 0.3091
  sharpe_ratio.................. 0.1847
  max_drawdown.................. -0.1234
  min_price..................... 95.2341
  max_price..................... 112.3456
  total_return.................. 8.5420
```

## Features Demonstrated

### Python Features
- Object-oriented design with clean module separation
- NumPy for numerical computing
- Pandas for data manipulation
- Matplotlib and Seaborn for visualization
- Statistical analysis with SciPy
- Command-line argument parsing

### OCaml Features
- Functional programming paradigm
- Immutable data structures
- Pattern matching
- List operations with higher-order functions
- Type safety and inference
- Standalone executable compilation

### Analytics Computed
- **Mean**: Average price and returns
- **Volatility**: Standard deviation of returns (daily and annualized)
- **Sharpe Ratio**: Risk-adjusted return metric
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Total Return**: Overall percentage change
- **Moving Averages**: Trend indicators
- **Bollinger Bands**: Volatility bands
- **RSI**: Momentum indicator

## Development

### Running Tests

Individual modules can be tested:

```bash
python src/data_fetcher.py
python src/analytics.py
python src/visualizer.py
```

### Extending the Project

Add new analytics functions in `src/analytics.py`:

```python
@staticmethod
def compute_new_metric(df: pd.DataFrame) -> float:
    # Your implementation
    pass
```

Add new visualizations in `src/visualizer.py`:

```python
def plot_new_chart(self, df: pd.DataFrame):
    # Your implementation
    pass
```

## Technical Notes

- Stock prices are generated using **Geometric Brownian Motion** (GBM)
- Volatility is annualized using √252 (trading days)
- Returns are calculated as logarithmic returns
- OCaml module uses functional list operations for all computations
- Python-OCaml interop via JSON and subprocess

## License

MIT License - Feel free to use and modify for your projects.

## Contributing

Contributions are welcome! Areas for enhancement:
- Real market data integration (API support)
- More technical indicators
- Machine learning predictions
- Portfolio optimization
- Backtesting framework
- Additional OCaml analytics functions

## Contact

For questions or suggestions, please open an issue on GitHub.