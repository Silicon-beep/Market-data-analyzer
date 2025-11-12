#!/usr/bin/env python3
"""
Quick Demo Script - Market Data Analyzer
Demonstrates all major features of the application
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from data_fetcher import MarketDataFetcher
from analytics import MarketAnalytics
from visualizer import MarketVisualizer


def demo_basic_analysis():
    """Demo 1: Basic single stock analysis"""
    print("\n" + "=" * 70)
    print("DEMO 1: Basic Single Stock Analysis")
    print("=" * 70)
    
    fetcher = MarketDataFetcher()
    analytics = MarketAnalytics()
    
    # Generate data
    print("\n📊 Generating market data for DEMO stock...")
    df = fetcher.generate_stock_prices("DEMO", days=100)
    
    print(f"✓ Generated {len(df)} data points")
    print(f"  Date range: {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}")
    
    # Compute analytics
    print("\n📈 Computing analytics...")
    report = analytics.generate_summary_report(df, "DEMO")
    
    print("\nKey Metrics:")
    print(f"  Mean Price:       ${report['mean_price']:.2f}")
    print(f"  Annual Volatility: {report['volatility_annual']:.2%}")
    print(f"  Sharpe Ratio:      {report['sharpe_ratio']:.3f}")
    print(f"  Total Return:      {report['total_return']:.2f}%")
    print(f"  Max Drawdown:      {report['max_drawdown']:.2%}")


def demo_multiple_stocks():
    """Demo 2: Multiple stock comparison"""
    print("\n" + "=" * 70)
    print("DEMO 2: Multiple Stock Comparison")
    print("=" * 70)
    
    fetcher = MarketDataFetcher()
    analytics = MarketAnalytics()
    
    symbols = ["AAPL", "GOOGL", "MSFT"]
    print(f"\n📊 Generating data for {len(symbols)} stocks: {', '.join(symbols)}")
    
    data_dict = fetcher.generate_multiple_stocks(symbols, days=100)
    
    print("\nComparative Analytics:")
    print("-" * 70)
    print(f"{'Stock':<10} {'Mean Price':<12} {'Volatility':<12} {'Return':<10}")
    print("-" * 70)
    
    for symbol, df in data_dict.items():
        report = analytics.generate_summary_report(df, symbol)
        print(f"{symbol:<10} ${report['mean_price']:<11.2f} {report['volatility_annual']:<11.2%} {report['total_return']:<9.2f}%")


def demo_technical_indicators():
    """Demo 3: Technical indicators"""
    print("\n" + "=" * 70)
    print("DEMO 3: Technical Indicators")
    print("=" * 70)
    
    fetcher = MarketDataFetcher()
    analytics = MarketAnalytics()
    
    print("\n📊 Generating data...")
    df = fetcher.generate_stock_prices("TECH", days=100)
    
    # Moving averages
    ma20 = analytics.compute_moving_average(df, window=20)
    ma50 = analytics.compute_moving_average(df, window=50)
    
    # Bollinger Bands
    middle, upper, lower = analytics.compute_bollinger_bands(df)
    
    # RSI
    rsi = analytics.compute_rsi(df)
    
    print("\n📈 Technical Indicators (Latest Values):")
    print(f"  Current Price:     ${df['Close'].iloc[-1]:.2f}")
    print(f"  20-Day MA:         ${ma20.iloc[-1]:.2f}")
    print(f"  50-Day MA:         ${ma50.iloc[-1]:.2f}")
    print(f"  Bollinger Upper:   ${upper.iloc[-1]:.2f}")
    print(f"  Bollinger Lower:   ${lower.iloc[-1]:.2f}")
    print(f"  RSI (14):          {rsi.iloc[-1]:.2f}")
    
    # Interpretation
    current_price = df['Close'].iloc[-1]
    current_rsi = rsi.iloc[-1]
    
    print("\n💡 Interpretation:")
    if current_rsi > 70:
        print("  RSI indicates OVERBOUGHT conditions")
    elif current_rsi < 30:
        print("  RSI indicates OVERSOLD conditions")
    else:
        print("  RSI indicates NEUTRAL conditions")
    
    if current_price > ma20.iloc[-1] and current_price > ma50.iloc[-1]:
        print("  Price above both MAs - BULLISH trend")
    elif current_price < ma20.iloc[-1] and current_price < ma50.iloc[-1]:
        print("  Price below both MAs - BEARISH trend")
    else:
        print("  Mixed signals - NEUTRAL trend")


def demo_risk_metrics():
    """Demo 4: Risk analysis"""
    print("\n" + "=" * 70)
    print("DEMO 4: Risk Analysis")
    print("=" * 70)
    
    fetcher = MarketDataFetcher()
    analytics = MarketAnalytics()
    
    print("\n📊 Generating data for two assets...")
    
    # Generate two assets with different characteristics
    safe_asset = fetcher.generate_stock_prices(
        "SAFE", days=252, initial_price=100, drift=0.0003, volatility=0.01
    )
    risky_asset = fetcher.generate_stock_prices(
        "RISKY", days=252, initial_price=100, drift=0.0005, volatility=0.03
    )
    
    safe_report = analytics.generate_summary_report(safe_asset, "SAFE")
    risky_report = analytics.generate_summary_report(risky_asset, "RISKY")
    
    print("\nRisk Comparison:")
    print("-" * 70)
    print(f"{'Metric':<25} {'Safe Asset':<20} {'Risky Asset':<20}")
    print("-" * 70)
    
    metrics = [
        ('Annual Volatility', 'volatility_annual', '%'),
        ('Sharpe Ratio', 'sharpe_ratio', ''),
        ('Max Drawdown', 'max_drawdown', '%'),
        ('Total Return', 'total_return', '%')
    ]
    
    for label, key, unit in metrics:
        safe_val = safe_report[key]
        risky_val = risky_report[key]
        
        if unit == '%':
            print(f"{label:<25} {safe_val:<19.2%} {risky_val:<19.2%}")
        else:
            print(f"{label:<25} {safe_val:<19.3f} {risky_val:<19.3f}")


def demo_ocaml_integration():
    """Demo 5: OCaml functional programming"""
    print("\n" + "=" * 70)
    print("DEMO 5: OCaml Functional Programming Integration")
    print("=" * 70)
    
    fetcher = MarketDataFetcher()
    analytics = MarketAnalytics()
    
    print("\n📊 Generating data...")
    df = fetcher.generate_stock_prices("FUNC", days=50)
    
    print("\n🔄 Computing analytics with Python...")
    py_report = analytics.generate_summary_report(df, "FUNC")
    
    print("\n🔄 Computing analytics with OCaml...")
    prices = df['Close'].tolist()
    ocaml_result = analytics.call_ocaml_analytics(prices)
    
    if ocaml_result:
        print("\n✓ OCaml module available!")
        print("\nComparison (Python vs OCaml):")
        print("-" * 70)
        print(f"{'Metric':<25} {'Python':<20} {'OCaml':<20}")
        print("-" * 70)
        
        comparisons = [
            ('Mean Price', 'mean_price'),
            ('Annual Volatility', 'volatility_annual'),
            ('Total Return', 'total_return'),
            ('Max Drawdown', 'max_drawdown')
        ]
        
        for label, key in comparisons:
            py_val = py_report.get(key, 0)
            ocaml_val = ocaml_result.get(key, 0)
            print(f"{label:<25} {py_val:<19.4f} {ocaml_val:<19.4f}")
        
        print("\n💡 Both implementations show similar results!")
        print("   Python: Object-oriented, extensive libraries")
        print("   OCaml: Functional, type-safe, compiled binary")
    else:
        print("\n⚠ OCaml module not available")
        print("  To enable: cd ocaml_analytics && ./build.sh")


def main():
    """Run all demos"""
    print("\n" + "=" * 70)
    print("   MARKET DATA ANALYZER - COMPREHENSIVE DEMO")
    print("=" * 70)
    print("\nThis demo showcases all major features:")
    print("  1. Basic analytics")
    print("  2. Multiple stock comparison")
    print("  3. Technical indicators")
    print("  4. Risk analysis")
    print("  5. Python-OCaml integration")
    print("\nNote: Visualizations are disabled in demo mode.")
    print("      Use main.py to see charts and graphs.")
    
    try:
        demo_basic_analysis()
        demo_multiple_stocks()
        demo_technical_indicators()
        demo_risk_metrics()
        demo_ocaml_integration()
        
        print("\n" + "=" * 70)
        print("✓ DEMO COMPLETE!")
        print("=" * 70)
        print("\nNext steps:")
        print("  • Run: python main.py --symbol AAPL --dashboard")
        print("  • Run: python main.py --symbols AAPL GOOGL MSFT")
        print("  • See README.md for more examples")
        print()
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
