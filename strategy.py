# strategy.py

import pandas as pd
import ta
from pocket_option_scraper import fetch_candles

def generate_signal(asset, timeframe):
    candles = fetch_candles(asset, timeframe, limit=100)
    if len(candles) < 50:
        return "WAIT", 0, "Not enough data"

    df = pd.DataFrame(candles)

    # Technical Indicators
    df['ema_fast'] = ta.trend.ema_indicator(df['close'], window=9)
    df['ema_slow'] = ta.trend.ema_indicator(df['close'], window=21)
    df['macd'] = ta.trend.macd(df['close'])
    df['macd_signal'] = ta.trend.macd_signal(df['close'])
    df['rsi'] = ta.momentum.rsi(df['close'], window=14)
    bb = ta.volatility.BollingerBands(df['close'], window=20, window_dev=2)
    df['bb_upper'] = bb.bollinger_hband()
    df['bb_lower'] = bb.bollinger_lband()

    # Last row analysis
    latest = df.iloc[-1]
    previous = df.iloc[-2]

    # Conditions
    ema_cross = latest['ema_fast'] > latest['ema_slow'] and previous['ema_fast'] <= previous['ema_slow']
    macd_cross = latest['macd'] > latest['macd_signal'] and previous['macd'] <= previous['macd_signal']
    rsi_ok = 45 < latest['rsi'] < 70
    bb_bounce = latest['close'] > latest['bb_lower'] and previous['close'] <= previous['bb_lower']

    # Combine signals
    if ema_cross and macd_cross and rsi_ok:
        return "BUY", 80, "EMA+MACD+RSI alignment"
    elif bb_bounce and rsi_ok:
        return "BUY", 70, "Bollinger Band bounce + RSI"

    # Bearish case
    ema_cross_down = latest['ema_fast'] < latest['ema_slow'] and previous['ema_fast'] >= previous['ema_slow']
    macd_cross_down = latest['macd'] < latest['macd_signal'] and previous['macd'] >= previous['macd_signal']
    rsi_low = 30 < latest['rsi'] < 55
    bb_bounce_top = latest['close'] < latest['bb_upper'] and previous['close'] >= previous['bb_upper']

    if ema_cross_down and macd_cross_down and rsi_low:
        return "SELL", 80, "EMA+MACD+RSI bearish alignment"
    elif bb_bounce_top and rsi_low:
        return "SELL", 70, "Bollinger Top Rejection + RSI"

    return "WAIT", 50, "No clear signal"
