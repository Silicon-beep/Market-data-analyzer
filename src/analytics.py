"""
Analytics Module
Computes various statistical metrics for market data
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
import subprocess
import json


class MarketAnalytics:
    """Computes analytics on market data"""
    
    @staticmethod
    def compute_returns(df: pd.DataFrame, price_col: str = 'Close') -> pd.Series:
        """
        Compute daily returns
        
        Args:
            df: DataFrame with price data
            price_col: Column name for prices
            
        Returns:
            Series of daily returns
        """
        return df[price_col].pct_change().dropna()
    
    @staticmethod
    def compute_mean(values: pd.Series) -> float:
        """
        Compute arithmetic mean
        
        Args:
            values: Series of values
            
        Returns:
            Mean value
        """
        return float(np.mean(values))
    
    @staticmethod
    def compute_volatility(returns: pd.Series, annualize: bool = True) -> float:
        """
        Compute volatility (standard deviation of returns)
        
        Args:
            returns: Series of returns
            annualize: If True, annualize the volatility (assuming 252 trading days)
            
        Returns:
            Volatility value
        """
        vol = float(np.std(returns))
        if annualize:
            vol *= np.sqrt(252)
        return vol
    
    @staticmethod
    def compute_sharpe_ratio(
        returns: pd.Series, 
        risk_free_rate: float = 0.02,
        annualize: bool = True
    ) -> float:
        """
        Compute Sharpe ratio
        
        Args:
            returns: Series of returns
            risk_free_rate: Annual risk-free rate
            annualize: If True, annualize the metrics
            
        Returns:
            Sharpe ratio
        """
        mean_return = np.mean(returns)
        std_return = np.std(returns)
        
        if annualize:
            mean_return = mean_return * 252
            std_return = std_return * np.sqrt(252)
        
        if std_return == 0:
            return 0.0
        
        return float((mean_return - risk_free_rate) / std_return)
    
    @staticmethod
    def compute_max_drawdown(df: pd.DataFrame, price_col: str = 'Close') -> float:
        """
        Compute maximum drawdown
        
        Args:
            df: DataFrame with price data
            price_col: Column name for prices
            
        Returns:
            Maximum drawdown as a percentage
        """
        prices = df[price_col]
        cumulative_max = prices.cummax()
        drawdown = (prices - cumulative_max) / cumulative_max
        return float(drawdown.min())
    
    @staticmethod
    def compute_moving_average(
        df: pd.DataFrame, 
        window: int = 20,
        price_col: str = 'Close'
    ) -> pd.Series:
        """
        Compute moving average
        
        Args:
            df: DataFrame with price data
            window: Window size for moving average
            price_col: Column name for prices
            
        Returns:
            Series of moving average values
        """
        return df[price_col].rolling(window=window).mean()
    
    @staticmethod
    def compute_bollinger_bands(
        df: pd.DataFrame,
        window: int = 20,
        num_std: float = 2.0,
        price_col: str = 'Close'
    ) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Compute Bollinger Bands
        
        Args:
            df: DataFrame with price data
            window: Window size for moving average
            num_std: Number of standard deviations for bands
            price_col: Column name for prices
            
        Returns:
            Tuple of (middle_band, upper_band, lower_band)
        """
        middle = df[price_col].rolling(window=window).mean()
        std = df[price_col].rolling(window=window).std()
        upper = middle + (std * num_std)
        lower = middle - (std * num_std)
        
        return middle, upper, lower
    
    @staticmethod
    def compute_rsi(
        df: pd.DataFrame,
        window: int = 14,
        price_col: str = 'Close'
    ) -> pd.Series:
        """
        Compute Relative Strength Index (RSI)
        
        Args:
            df: DataFrame with price data
            window: Window size for RSI calculation
            price_col: Column name for prices
            
        Returns:
            Series of RSI values
        """
        delta = df[price_col].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def generate_summary_report(
        self,
        df: pd.DataFrame,
        symbol: str = "STOCK"
    ) -> Dict:
        """
        Generate comprehensive analytics report
        
        Args:
            df: DataFrame with price data
            symbol: Stock symbol
            
        Returns:
            Dictionary with analytics metrics
        """
        returns = self.compute_returns(df)
        
        report = {
            'symbol': symbol,
            'period': f"{df['Date'].min()} to {df['Date'].max()}",
            'total_days': len(df),
            'mean_price': self.compute_mean(df['Close']),
            'mean_daily_return': self.compute_mean(returns),
            'volatility_daily': self.compute_volatility(returns, annualize=False),
            'volatility_annual': self.compute_volatility(returns, annualize=True),
            'sharpe_ratio': self.compute_sharpe_ratio(returns),
            'max_drawdown': self.compute_max_drawdown(df),
            'min_price': float(df['Close'].min()),
            'max_price': float(df['Close'].max()),
            'total_return': float((df['Close'].iloc[-1] / df['Close'].iloc[0] - 1) * 100)
        }
        
        return report
    
    @staticmethod
    def call_ocaml_analytics(prices: List[float]) -> Optional[Dict]:
        """
        Call OCaml module for computing analytics
        
        Args:
            prices: List of price values
            
        Returns:
            Dictionary with OCaml-computed metrics or None if OCaml not available
        """
        try:
            # Save prices to temporary file
            with open('/tmp/market_prices.json', 'w') as f:
                json.dump(prices, f)
            
            # Call OCaml binary (if compiled)
            result = subprocess.run(
                ['./ocaml_analytics/analytics.exe', '/tmp/market_prices.json'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return None
                
        except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError):
            return None


if __name__ == "__main__":
    # Demo usage
    from data_fetcher import MarketDataFetcher
    
    fetcher = MarketDataFetcher()
    df = fetcher.generate_stock_prices("DEMO", days=100)
    
    analytics = MarketAnalytics()
    report = analytics.generate_summary_report(df, "DEMO")
    
    print("Analytics Report:")
    print("=" * 50)
    for key, value in report.items():
        if isinstance(value, float):
            print(f"{key}: {value:.4f}")
        else:
            print(f"{key}: {value}")
