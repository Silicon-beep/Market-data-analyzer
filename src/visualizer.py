"""
Visualization Module
Creates charts and graphs for market data analysis
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from typing import Optional, Tuple
import seaborn as sns


class MarketVisualizer:
    """Creates visualizations for market data"""
    
    def __init__(self, style: str = 'seaborn-v0_8-darkgrid'):
        """
        Initialize visualizer
        
        Args:
            style: Matplotlib style to use
        """
        try:
            plt.style.use(style)
        except:
            plt.style.use('default')
        
        sns.set_palette("husl")
    
    def plot_price_history(
        self,
        df: pd.DataFrame,
        symbol: str = "STOCK",
        figsize: Tuple[int, int] = (12, 6),
        save_path: Optional[str] = None
    ):
        """
        Plot price history with OHLC data
        
        Args:
            df: DataFrame with price data
            symbol: Stock symbol
            figsize: Figure size
            save_path: Path to save figure (if provided)
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        ax.plot(df['Date'], df['Close'], label='Close', linewidth=2)
        ax.fill_between(df['Date'], df['Low'], df['High'], alpha=0.3, label='High-Low Range')
        
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Price ($)', fontsize=12)
        ax.set_title(f'{symbol} - Price History', fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved plot to {save_path}")
        
        plt.show()
    
    def plot_returns_distribution(
        self,
        returns: pd.Series,
        symbol: str = "STOCK",
        figsize: Tuple[int, int] = (10, 6),
        save_path: Optional[str] = None
    ):
        """
        Plot distribution of returns
        
        Args:
            returns: Series of returns
            symbol: Stock symbol
            figsize: Figure size
            save_path: Path to save figure
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        
        # Histogram
        ax1.hist(returns, bins=50, edgecolor='black', alpha=0.7)
        ax1.axvline(returns.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {returns.mean():.4f}')
        ax1.set_xlabel('Daily Returns', fontsize=12)
        ax1.set_ylabel('Frequency', fontsize=12)
        ax1.set_title(f'{symbol} - Returns Distribution', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Q-Q plot
        from scipy import stats
        stats.probplot(returns, dist="norm", plot=ax2)
        ax2.set_title(f'{symbol} - Q-Q Plot', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved plot to {save_path}")
        
        plt.show()
    
    def plot_moving_averages(
        self,
        df: pd.DataFrame,
        ma_windows: list = [20, 50],
        symbol: str = "STOCK",
        figsize: Tuple[int, int] = (12, 6),
        save_path: Optional[str] = None
    ):
        """
        Plot price with moving averages
        
        Args:
            df: DataFrame with price data
            ma_windows: List of window sizes for moving averages
            symbol: Stock symbol
            figsize: Figure size
            save_path: Path to save figure
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        ax.plot(df['Date'], df['Close'], label='Close Price', linewidth=2, alpha=0.7)
        
        for window in ma_windows:
            ma = df['Close'].rolling(window=window).mean()
            ax.plot(df['Date'], ma, label=f'{window}-Day MA', linewidth=1.5)
        
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Price ($)', fontsize=12)
        ax.set_title(f'{symbol} - Price with Moving Averages', fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved plot to {save_path}")
        
        plt.show()
    
    def plot_bollinger_bands(
        self,
        df: pd.DataFrame,
        window: int = 20,
        num_std: float = 2.0,
        symbol: str = "STOCK",
        figsize: Tuple[int, int] = (12, 6),
        save_path: Optional[str] = None
    ):
        """
        Plot Bollinger Bands
        
        Args:
            df: DataFrame with price data
            window: Window size
            num_std: Number of standard deviations
            symbol: Stock symbol
            figsize: Figure size
            save_path: Path to save figure
        """
        from analytics import MarketAnalytics
        
        middle, upper, lower = MarketAnalytics.compute_bollinger_bands(df, window, num_std)
        
        fig, ax = plt.subplots(figsize=figsize)
        
        ax.plot(df['Date'], df['Close'], label='Close Price', linewidth=2, color='black')
        ax.plot(df['Date'], middle, label=f'{window}-Day MA', linewidth=1.5, color='blue')
        ax.plot(df['Date'], upper, label='Upper Band', linewidth=1, linestyle='--', color='red')
        ax.plot(df['Date'], lower, label='Lower Band', linewidth=1, linestyle='--', color='green')
        ax.fill_between(df['Date'], lower, upper, alpha=0.1, color='gray')
        
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Price ($)', fontsize=12)
        ax.set_title(f'{symbol} - Bollinger Bands ({window} days, {num_std}σ)', fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved plot to {save_path}")
        
        plt.show()
    
    def plot_volatility(
        self,
        returns: pd.Series,
        window: int = 20,
        symbol: str = "STOCK",
        figsize: Tuple[int, int] = (12, 6),
        save_path: Optional[str] = None
    ):
        """
        Plot rolling volatility
        
        Args:
            returns: Series of returns
            window: Window size for rolling volatility
            symbol: Stock symbol
            figsize: Figure size
            save_path: Path to save figure
        """
        rolling_vol = returns.rolling(window=window).std() * np.sqrt(252)  # Annualized
        
        fig, ax = plt.subplots(figsize=figsize)
        
        ax.plot(rolling_vol.index, rolling_vol, linewidth=2, color='purple')
        ax.axhline(rolling_vol.mean(), color='red', linestyle='--', 
                   linewidth=2, label=f'Mean: {rolling_vol.mean():.4f}')
        
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Annualized Volatility', fontsize=12)
        ax.set_title(f'{symbol} - Rolling {window}-Day Volatility', fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved plot to {save_path}")
        
        plt.show()
    
    def plot_multiple_stocks(
        self,
        data_dict: dict,
        normalize: bool = True,
        figsize: Tuple[int, int] = (12, 6),
        save_path: Optional[str] = None
    ):
        """
        Plot multiple stocks on same chart
        
        Args:
            data_dict: Dictionary mapping symbols to DataFrames
            normalize: If True, normalize prices to start at 100
            figsize: Figure size
            save_path: Path to save figure
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        for symbol, df in data_dict.items():
            if normalize:
                normalized_price = (df['Close'] / df['Close'].iloc[0]) * 100
                ax.plot(df['Date'], normalized_price, label=symbol, linewidth=2)
            else:
                ax.plot(df['Date'], df['Close'], label=symbol, linewidth=2)
        
        ax.set_xlabel('Date', fontsize=12)
        ylabel = 'Normalized Price (Base=100)' if normalize else 'Price ($)'
        ax.set_ylabel(ylabel, fontsize=12)
        ax.set_title('Multiple Stocks Comparison', fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved plot to {save_path}")
        
        plt.show()
    
    def create_dashboard(
        self,
        df: pd.DataFrame,
        symbol: str = "STOCK",
        figsize: Tuple[int, int] = (16, 10),
        save_path: Optional[str] = None
    ):
        """
        Create comprehensive dashboard with multiple plots
        
        Args:
            df: DataFrame with price data
            symbol: Stock symbol
            figsize: Figure size
            save_path: Path to save figure
        """
        from analytics import MarketAnalytics
        
        analytics = MarketAnalytics()
        returns = analytics.compute_returns(df)
        
        fig = plt.figure(figsize=figsize)
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        # Price history
        ax1 = fig.add_subplot(gs[0, :])
        ax1.plot(df['Date'], df['Close'], linewidth=2, color='blue')
        ax1.set_title(f'{symbol} - Price History', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Price ($)')
        ax1.grid(True, alpha=0.3)
        
        # Returns distribution
        ax2 = fig.add_subplot(gs[1, 0])
        ax2.hist(returns, bins=30, edgecolor='black', alpha=0.7, color='green')
        ax2.axvline(returns.mean(), color='red', linestyle='--', linewidth=2)
        ax2.set_title('Returns Distribution', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Daily Returns')
        ax2.set_ylabel('Frequency')
        ax2.grid(True, alpha=0.3)
        
        # Volatility
        ax3 = fig.add_subplot(gs[1, 1])
        rolling_vol = returns.rolling(window=20).std() * np.sqrt(252)
        rolling_vol = rolling_vol.dropna()
        vol_dates = df['Date'][len(df) - len(rolling_vol):]
        ax3.plot(vol_dates, rolling_vol, linewidth=2, color='purple')
        ax3.set_title('20-Day Rolling Volatility', fontsize=12, fontweight='bold')
        ax3.set_ylabel('Annualized Volatility')
        ax3.grid(True, alpha=0.3)
        
        # Moving averages
        ax4 = fig.add_subplot(gs[2, 0])
        ax4.plot(df['Date'], df['Close'], label='Close', linewidth=2, alpha=0.7)
        ma20 = df['Close'].rolling(window=20).mean()
        ma50 = df['Close'].rolling(window=50).mean()
        ax4.plot(df['Date'], ma20, label='20-Day MA', linewidth=1.5)
        ax4.plot(df['Date'], ma50, label='50-Day MA', linewidth=1.5)
        ax4.set_title('Moving Averages', fontsize=12, fontweight='bold')
        ax4.set_ylabel('Price ($)')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # Volume
        ax5 = fig.add_subplot(gs[2, 1])
        ax5.bar(df['Date'], df['Volume'], alpha=0.7, color='orange')
        ax5.set_title('Trading Volume', fontsize=12, fontweight='bold')
        ax5.set_ylabel('Volume')
        ax5.grid(True, alpha=0.3)
        
        fig.suptitle(f'{symbol} - Market Analysis Dashboard', fontsize=16, fontweight='bold', y=0.995)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved dashboard to {save_path}")
        
        plt.show()


if __name__ == "__main__":
    # Demo usage
    from data_fetcher import MarketDataFetcher
    
    fetcher = MarketDataFetcher()
    df = fetcher.generate_stock_prices("DEMO", days=200)
    
    viz = MarketVisualizer()
    viz.plot_price_history(df, "DEMO")
