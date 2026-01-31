"""
Helper script to plot historical candles and Prophet forecasts
for tickers from the `HyperliquidForecaster` class in `forecaster.py`.

Usage (PowerShell):
    python .\plot_forecaster.py --coin BTC --interval 1h --periods 24

Requirements:
    pip install matplotlib prophet pandas hyperliquid-client

The script uses the existing `HyperliquidForecaster._fetch_candles`
method to get historical data, fits a Prophet model and plots:
    - historical series
    - forecast (yhat)
    - confidence interval (yhat_lower, yhat_upper)
    - a vertical line marking the last observed timestamp

"""

import argparse
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from prophet import Prophet

from forecaster import HyperliquidForecaster


def plot_forecast(coin: str, interval: str = "1h", periods: int = 24, testnet: bool = True,
                  figsize=(12, 6), save_path: str = None, show: bool = True):
    """Fetch data, fit Prophet and plot historical + forecast.

    Returns (forecast_df, history_df)
    """
    # Create forecaster instance (uses hyperliquid info client)
    f = HyperliquidForecaster(testnet=testnet)

    # determine freq and limits consistent with forecaster._fetch_candles
    if interval == "15m":
        limit = 300
        freq = "15min"
    else:
        limit = 500
        freq = "H"

    # Get historical candles (DataFrame with columns ds, y)
    hist = f._fetch_candles(coin, interval, limit)

    # Fit Prophet on historical
    model = Prophet(daily_seasonality=True, weekly_seasonality=True)
    model.fit(hist)

    # Make future dataframe and predict
    future = model.make_future_dataframe(periods=periods, freq=freq)
    forecast = model.predict(future)

    # Plot
    plt.figure(figsize=figsize)
    plt.plot(hist['ds'], hist['y'], label='Historical', color='black')

    # Forecast line and CI
    plt.plot(forecast['ds'], forecast['yhat'], label='Forecast (yhat)', color='tab:blue')
    plt.fill_between(forecast['ds'].dt.to_pydatetime(),
                     forecast['yhat_lower'],
                     forecast['yhat_upper'],
                     color='tab:blue', alpha=0.2, label='Confidence interval')

    # mark last observed
    last_obs_dt = hist['ds'].iloc[-1]
    plt.axvline(last_obs_dt, color='gray', linestyle='--', label='Last observed')

    plt.title(f"{coin} - {interval} forecast ({periods} periods)")
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches='tight')

    if show:
        plt.show()
    else:
        plt.close()

    return forecast, hist


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot Hyperliquid forecasts using Prophet')
    parser.add_argument('--coin', type=str, default='BTC', help='Ticker name (e.g. BTC, ETH)')
    parser.add_argument('--interval', type=str, choices=['15m', '1h'], default='1h', help='Candle interval')
    parser.add_argument('--periods', type=int, default=24, help='Number of future periods to predict/plot')
    parser.add_argument('--testnet', action='store_true', help='Use testnet endpoints')
    parser.add_argument('--save', type=str, default=None, help='Save plot to this path instead of showing')
    args = parser.parse_args()

    try:
        plot_forecast(args.coin, args.interval, args.periods, testnet=args.testnet, save_path=args.save, show=(args.save is None))
    except Exception as e:
        print(f"Plot failed: {e}")
