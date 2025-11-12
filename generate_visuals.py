#!/usr/bin/env python3
"""
Visual Demo - Generate Multiple Charts for Display
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from data_fetcher import MarketDataFetcher
from analytics import MarketAnalytics
from visualizer import MarketVisualizer

print("=" * 70)
print("GENERATING VISUALIZATIONS - Market Data Analyzer")
print("=" * 70)
print()

# Initialize components
fetcher = MarketDataFetcher()
analytics = MarketAnalytics()
viz = MarketVisualizer()

# 1. Generate data for a single stock
print("1️⃣  Generating AAPL stock data (180 days)...")
df_aapl = fetcher.generate_stock_prices("AAPL", days=180)
print(f"   ✓ Generated {len(df_aapl)} data points")

# 2. Create price history chart
print("\n2️⃣  Creating Price History Chart...")
viz.plot_price_history(df_aapl, "AAPL", save_path="/tmp/viz_price_history.png")
print("   ✓ Saved: /tmp/viz_price_history.png")

# 3. Create returns distribution
print("\n3️⃣  Creating Returns Distribution...")
returns = analytics.compute_returns(df_aapl)
viz.plot_returns_distribution(returns, "AAPL", save_path="/tmp/viz_returns_dist.png")
print("   ✓ Saved: /tmp/viz_returns_dist.png")

# 4. Create moving averages chart
print("\n4️⃣  Creating Moving Averages Chart...")
viz.plot_moving_averages(df_aapl, ma_windows=[20, 50], symbol="AAPL", 
                         save_path="/tmp/viz_moving_averages.png")
print("   ✓ Saved: /tmp/viz_moving_averages.png")

# 5. Create Bollinger Bands chart
print("\n5️⃣  Creating Bollinger Bands Chart...")
viz.plot_bollinger_bands(df_aapl, symbol="AAPL", 
                         save_path="/tmp/viz_bollinger_bands.png")
print("   ✓ Saved: /tmp/viz_bollinger_bands.png")

# 6. Create volatility chart
print("\n6️⃣  Creating Volatility Chart...")
viz.plot_volatility(returns, window=20, symbol="AAPL", 
                    save_path="/tmp/viz_volatility.png")
print("   ✓ Saved: /tmp/viz_volatility.png")

# 7. Generate multiple stocks for comparison
print("\n7️⃣  Generating Multiple Stocks for Comparison...")
stocks = fetcher.generate_multiple_stocks(["AAPL", "GOOGL", "MSFT"], days=180)
print(f"   ✓ Generated {len(stocks)} stocks")

print("\n8️⃣  Creating Multi-Stock Comparison Chart...")
viz.plot_multiple_stocks(stocks, normalize=True, 
                         save_path="/tmp/viz_multi_stock.png")
print("   ✓ Saved: /tmp/viz_multi_stock.png")

# 8. Create comprehensive dashboard
print("\n9️⃣  Creating Comprehensive Dashboard (6 panels)...")
viz.create_dashboard(df_aapl, symbol="AAPL", 
                     save_path="/tmp/viz_dashboard.png")
print("   ✓ Saved: /tmp/viz_dashboard.png")

print("\n" + "=" * 70)
print("✅ ALL VISUALIZATIONS GENERATED!")
print("=" * 70)
print("\nGenerated Files:")
print("-" * 70)

import os
viz_files = [
    "/tmp/viz_price_history.png",
    "/tmp/viz_returns_dist.png", 
    "/tmp/viz_moving_averages.png",
    "/tmp/viz_bollinger_bands.png",
    "/tmp/viz_volatility.png",
    "/tmp/viz_multi_stock.png",
    "/tmp/viz_dashboard.png"
]

for i, file in enumerate(viz_files, 1):
    if os.path.exists(file):
        size = os.path.getsize(file) / 1024  # KB
        print(f"{i}. {file}")
        print(f"   Size: {size:.1f} KB")

print("\n" + "=" * 70)
print("📊 You can view these PNG files in your file browser")
print("=" * 70)
