"""
Market Data Fetcher Module
Generates sample market data for analysis
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict


class MarketDataFetcher:
    """Fetches and generates sample market data"""
    
    def __init__(self, seed: int = 42):
        """
        Initialize the data fetcher
        
        Args:
            seed: Random seed for reproducibility
        """
        np.random.seed(seed)
    
    def generate_stock_prices(
        self, 
        symbol: str,
        days: int = 252,
        initial_price: float = 100.0,
        drift: float = 0.0002,
        volatility: float = 0.02
    ) -> pd.DataFrame:
        """
        Generate synthetic stock price data using Geometric Brownian Motion
        
        Args:
            symbol: Stock ticker symbol
            days: Number of trading days to generate
            initial_price: Starting stock price
            drift: Daily drift rate
            volatility: Daily volatility
            
        Returns:
            DataFrame with Date, Symbol, Open, High, Low, Close, Volume
        """
        # Generate dates
        start_date = datetime.now() - timedelta(days=days)
        dates = pd.date_range(start=start_date, periods=days, freq='B')
        
        # Generate prices using Geometric Brownian Motion
        returns = np.random.normal(drift, volatility, days)
        prices = initial_price * np.exp(np.cumsum(returns))
        
        # Generate OHLC data
        data = {
            'Date': dates,
            'Symbol': symbol,
            'Open': prices * (1 + np.random.uniform(-0.005, 0.005, days)),
            'High': prices * (1 + np.abs(np.random.uniform(0, 0.01, days))),
            'Low': prices * (1 - np.abs(np.random.uniform(0, 0.01, days))),
            'Close': prices,
            'Volume': np.random.randint(1000000, 10000000, days)
        }
        
        df = pd.DataFrame(data)
        
        # Ensure High is highest and Low is lowest
        df['High'] = df[['Open', 'High', 'Close']].max(axis=1)
        df['Low'] = df[['Open', 'Low', 'Close']].min(axis=1)
        
        return df
    
    def generate_multiple_stocks(
        self,
        symbols: List[str],
        days: int = 252
    ) -> Dict[str, pd.DataFrame]:
        """
        Generate data for multiple stocks
        
        Args:
            symbols: List of stock ticker symbols
            days: Number of trading days
            
        Returns:
            Dictionary mapping symbols to DataFrames
        """
        data = {}
        for i, symbol in enumerate(symbols):
            # Vary parameters for different stocks
            initial_price = np.random.uniform(50, 200)
            drift = np.random.uniform(-0.0005, 0.001)
            volatility = np.random.uniform(0.01, 0.03)
            
            data[symbol] = self.generate_stock_prices(
                symbol=symbol,
                days=days,
                initial_price=initial_price,
                drift=drift,
                volatility=volatility
            )
        
        return data
    
    def save_to_csv(self, df: pd.DataFrame, filename: str):
        """
        Save data to CSV file
        
        Args:
            df: DataFrame to save
            filename: Output filename
        """
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    
    def load_from_csv(self, filename: str) -> pd.DataFrame:
        """
        Load data from CSV file
        
        Args:
            filename: Input filename
            
        Returns:
            DataFrame with market data
        """
        df = pd.read_csv(filename, parse_dates=['Date'])
        return df


if __name__ == "__main__":
    # Demo usage
    fetcher = MarketDataFetcher()
    
    # Generate single stock
    aapl_data = fetcher.generate_stock_prices("AAPL", days=100)
    print("Generated AAPL data:")
    print(aapl_data.head())
    print(f"\nShape: {aapl_data.shape}")
    
    # Generate multiple stocks
    stocks = fetcher.generate_multiple_stocks(["AAPL", "GOOGL", "MSFT"], days=50)
    print(f"\nGenerated {len(stocks)} stocks")
