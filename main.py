#!/usr/bin/env python3
"""
Market Data Analyzer - Main Application
Demonstrates the complete workflow: data fetching, analytics, and visualization
"""

import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from data_fetcher import MarketDataFetcher
from analytics import MarketAnalytics
from visualizer import MarketVisualizer


def main():
    """Main application entry point"""
    
    parser = argparse.ArgumentParser(
        description='Market Data Analyzer - Analyze stock market data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze single stock with default parameters
  python main.py --symbol AAPL
  
  # Analyze multiple stocks
  python main.py --symbols AAPL GOOGL MSFT --days 180
  
  # Generate full dashboard
  python main.py --symbol TSLA --dashboard
  
  # Save outputs to files
  python main.py --symbol NVDA --save-csv data.csv --save-plot plot.png
        """
    )
    
    parser.add_argument(
        '--symbol', 
        type=str, 
        default='STOCK',
        help='Single stock symbol to analyze (default: STOCK)'
    )
    
    parser.add_argument(
        '--symbols',
        type=str,
        nargs='+',
        help='Multiple stock symbols to compare'
    )
    
    parser.add_argument(
        '--days',
        type=int,
        default=252,
        help='Number of trading days to generate (default: 252)'
    )
    
    parser.add_argument(
        '--dashboard',
        action='store_true',
        help='Create comprehensive dashboard'
    )
    
    parser.add_argument(
        '--save-csv',
        type=str,
        help='Save data to CSV file'
    )
    
    parser.add_argument(
        '--save-plot',
        type=str,
        help='Save plot to file'
    )
    
    parser.add_argument(
        '--no-plot',
        action='store_true',
        help='Skip plotting (only show analytics)'
    )
    
    parser.add_argument(
        '--use-ocaml',
        action='store_true',
        help='Use OCaml module for analytics computation'
    )
    
    args = parser.parse_args()
    
    # Initialize components
    print("=" * 60)
    print("Market Data Analyzer")
    print("=" * 60)
    print()
    
    fetcher = MarketDataFetcher()
    analytics = MarketAnalytics()
    visualizer = MarketVisualizer()
    
    # Handle multiple stocks comparison
    if args.symbols:
        print(f"Analyzing {len(args.symbols)} stocks: {', '.join(args.symbols)}")
        print(f"Period: {args.days} trading days")
        print()
        
        # Generate data for multiple stocks
        data_dict = fetcher.generate_multiple_stocks(args.symbols, days=args.days)
        
        # Print analytics for each stock
        for symbol, df in data_dict.items():
            print(f"\n{'=' * 60}")
            print(f"Analytics Report: {symbol}")
            print('=' * 60)
            
            report = analytics.generate_summary_report(df, symbol)
            for key, value in report.items():
                if isinstance(value, float):
                    print(f"  {key:.<30} {value:.4f}")
                else:
                    print(f"  {key:.<30} {value}")
        
        # Visualize comparison
        if not args.no_plot:
            print("\nGenerating comparison chart...")
            visualizer.plot_multiple_stocks(
                data_dict,
                normalize=True,
                save_path=args.save_plot
            )
        
        return
    
    # Single stock analysis
    symbol = args.symbol
    print(f"Generating data for {symbol}...")
    print(f"Period: {args.days} trading days")
    print()
    
    # Generate data
    df = fetcher.generate_stock_prices(
        symbol=symbol,
        days=args.days
    )
    
    print(f"Generated {len(df)} data points")
    print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
    print()
    
    # Save to CSV if requested
    if args.save_csv:
        fetcher.save_to_csv(df, args.save_csv)
        print()
    
    # Compute analytics
    print("=" * 60)
    print("Analytics Report")
    print("=" * 60)
    
    report = analytics.generate_summary_report(df, symbol)
    
    for key, value in report.items():
        if isinstance(value, float):
            print(f"  {key:.<30} {value:.4f}")
        else:
            print(f"  {key:.<30} {value}")
    
    # Try OCaml analytics if requested
    if args.use_ocaml:
        print("\n" + "=" * 60)
        print("OCaml Analytics (Functional Programming)")
        print("=" * 60)
        
        prices = df['Close'].tolist()
        ocaml_result = analytics.call_ocaml_analytics(prices)
        
        if ocaml_result:
            for key, value in ocaml_result.items():
                print(f"  {key:.<30} {value:.4f}")
        else:
            print("  OCaml module not available or not compiled.")
            print("  Run: cd ocaml_analytics && ./build.sh")
    
    print()
    
    # Visualization
    if not args.no_plot:
        if args.dashboard:
            print("Creating comprehensive dashboard...")
            visualizer.create_dashboard(
                df,
                symbol=symbol,
                save_path=args.save_plot
            )
        else:
            print("Creating visualizations...")
            
            # Price history
            visualizer.plot_price_history(
                df,
                symbol=symbol,
                save_path=args.save_plot
            )
            
            # Additional plots
            returns = analytics.compute_returns(df)
            
            # Moving averages
            visualizer.plot_moving_averages(
                df,
                ma_windows=[20, 50],
                symbol=symbol
            )
            
            # Bollinger Bands
            visualizer.plot_bollinger_bands(
                df,
                symbol=symbol
            )
    
    print("\nAnalysis complete!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
