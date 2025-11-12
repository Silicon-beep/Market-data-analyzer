#!/usr/bin/env python3
"""
Web Interface for Market Data Analyzer
Flask-based web application to display visualizations and run analysis
"""

from flask import Flask, render_template, request, jsonify, send_file
import sys
from pathlib import Path
import os
import json
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from data_fetcher import MarketDataFetcher
from analytics import MarketAnalytics
from visualizer import MarketVisualizer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'market-data-analyzer-2025'

# Create visualizations directory
VIZ_DIR = Path(__file__).parent / 'static' / 'images'
VIZ_DIR.mkdir(parents=True, exist_ok=True)

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_analysis():
    """Generate new analysis based on user input"""
    try:
        data = request.json
        symbol = data.get('symbol', 'AAPL').upper()
        days = int(data.get('days', 180))
        use_real_data = data.get('use_real_data', True)
        
        # Initialize components
        fetcher = MarketDataFetcher()
        analytics = MarketAnalytics()
        viz = MarketVisualizer()
        
        # Get data - try real data first, fallback to simulated
        if use_real_data:
            try:
                # Download real market data using yfinance
                print(f"Fetching real data for {symbol}...")
                ticker = yf.Ticker(symbol)
                end_date = datetime.now()
                start_date = end_date - timedelta(days=days + 50)  # Extra buffer for trading days
                
                hist = ticker.history(start=start_date, end=end_date)
                
                if len(hist) > 0:
                    # Convert to our format
                    df = pd.DataFrame({
                        'Date': hist.index,
                        'Symbol': symbol,
                        'Open': hist['Open'],
                        'High': hist['High'],
                        'Low': hist['Low'],
                        'Close': hist['Close'],
                        'Volume': hist['Volume']
                    })
                    df = df.tail(days)  # Get last N days
                    data_source = "Real Market Data (Yahoo Finance)"
                    print(f"✓ Got {len(df)} days of real data for {symbol}")
                else:
                    raise ValueError("No data available")
                    
            except Exception as e:
                print(f"⚠ Could not fetch real data: {e}. Using simulated data.")
                df = fetcher.generate_stock_prices(symbol, days=days)
                data_source = "Simulated Data (Geometric Brownian Motion)"
        else:
            df = fetcher.generate_stock_prices(symbol, days=days)
            data_source = "Simulated Data (Geometric Brownian Motion)"
        
        # Compute analytics
        report = analytics.generate_summary_report(df, symbol)
        
        # Generate visualizations
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        viz_files = {
            'price': f'price_{symbol}_{timestamp}.png',
            'returns': f'returns_{symbol}_{timestamp}.png',
            'ma': f'ma_{symbol}_{timestamp}.png',
            'bollinger': f'bollinger_{symbol}_{timestamp}.png',
            'volatility': f'volatility_{symbol}_{timestamp}.png',
            'dashboard': f'dashboard_{symbol}_{timestamp}.png'
        }
        
        # Generate each visualization
        print(f"Generating visualizations for {symbol}...")
        viz.plot_price_history(df, symbol, save_path=str(VIZ_DIR / viz_files['price']))
        
        returns = analytics.compute_returns(df)
        viz.plot_returns_distribution(returns, symbol, save_path=str(VIZ_DIR / viz_files['returns']))
        
        viz.plot_moving_averages(df, symbol=symbol, save_path=str(VIZ_DIR / viz_files['ma']))
        
        viz.plot_bollinger_bands(df, symbol=symbol, save_path=str(VIZ_DIR / viz_files['bollinger']))
        
        viz.plot_volatility(returns, symbol=symbol, save_path=str(VIZ_DIR / viz_files['volatility']))
        
        viz.create_dashboard(df, symbol=symbol, save_path=str(VIZ_DIR / viz_files['dashboard']))
        
        print(f"✓ All visualizations generated for {symbol}")
        
        # Prepare response
        response = {
            'success': True,
            'symbol': symbol,
            'days': len(df),
            'data_source': data_source,
            'date_range': f"{df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}",
            'report': {
                'mean_price': f"${report['mean_price']:.2f}",
                'volatility_annual': f"{report['volatility_annual']:.2%}",
                'sharpe_ratio': f"{report['sharpe_ratio']:.3f}",
                'max_drawdown': f"{report['max_drawdown']:.2%}",
                'total_return': f"{report['total_return']:.2f}%",
                'min_price': f"${report['min_price']:.2f}",
                'max_price': f"${report['max_price']:.2f}"
            },
            'visualizations': {k: f'/static/images/{v}' for k, v in viz_files.items()}
        }
        
        return jsonify(response)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/compare', methods=['POST'])
def compare_stocks():
    """Compare multiple stocks"""
    try:
        data = request.json
        symbols_input = data.get('symbols', 'AAPL,GOOGL,MSFT')
        # Handle both string and list inputs
        if isinstance(symbols_input, str):
            symbols = [s.strip().upper() for s in symbols_input.split(',') if s.strip()]
        else:
            symbols = [s.strip().upper() for s in symbols_input if s.strip()]
        days = int(data.get('days', 180))
        use_real_data = data.get('use_real_data', True)
        
        fetcher = MarketDataFetcher()
        analytics = MarketAnalytics()
        viz = MarketVisualizer()
        
        stock_data = {}
        data_sources = {}
        
        # Get data for each stock
        for symbol in symbols:
            if use_real_data:
                try:
                    print(f"Fetching real data for {symbol}...")
                    ticker = yf.Ticker(symbol)
                    end_date = datetime.now()
                    start_date = end_date - timedelta(days=days + 50)
                    
                    hist = ticker.history(start=start_date, end=end_date)
                    
                    if len(hist) > 0:
                        df = pd.DataFrame({
                            'Date': hist.index,
                            'Symbol': symbol,
                            'Open': hist['Open'],
                            'High': hist['High'],
                            'Low': hist['Low'],
                            'Close': hist['Close'],
                            'Volume': hist['Volume']
                        })
                        df = df.tail(days)
                        stock_data[symbol] = df
                        data_sources[symbol] = "Real"
                        print(f"✓ Got {len(df)} days of real data for {symbol}")
                    else:
                        raise ValueError("No data")
                except Exception as e:
                    print(f"⚠ Using simulated data for {symbol}: {e}")
                    stock_data[symbol] = fetcher.generate_stock_prices(symbol, days=days)
                    data_sources[symbol] = "Simulated"
            else:
                stock_data[symbol] = fetcher.generate_stock_prices(symbol, days=days)
                data_sources[symbol] = "Simulated"
        
        # Generate comparison chart
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        comparison_file = f'comparison_{timestamp}.png'
        viz.plot_multiple_stocks(stock_data, normalize=True, 
                                save_path=str(VIZ_DIR / comparison_file))
        
        # Get analytics for each stock
        reports = {}
        for symbol, df in stock_data.items():
            report = analytics.generate_summary_report(df, symbol)
            reports[symbol] = {
                'mean_price': f"${report['mean_price']:.2f}",
                'volatility': f"{report['volatility_annual']:.2%}",
                'return': f"{report['total_return']:.2f}%",
                'sharpe': f"{report['sharpe_ratio']:.3f}",
                'data_source': data_sources[symbol]
            }
        
        print(f"✓ Comparison complete for {', '.join(symbols)}")
        
        return jsonify({
            'success': True,
            'symbols': symbols,
            'reports': reports,
            'visualization': f'/static/images/{comparison_file}'
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 70)
    print("🌐 Market Data Analyzer - Web Interface")
    print("=" * 70)
    print("\nStarting Flask web server...")
    print("Access the application at: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 70)
    app.run(debug=True, host='0.0.0.0', port=5000)
