# strategy.py

import pandas as pd
import numpy as np
from ta.trend import EMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
from pocket_option_scraper import get_candles

def generate_signal(asset, timeframe):
    df = get_candles(asset, timeframe)

    if not isinstance(df, pd.DataFrame) or len(df) < 50:
        return None, 0, "Insufficient data"

    df = df.copy()
    df['close'] = pd.to_numeric(df['close'], errors='coerce')

    # === Indicators ===
    macd = MACD(df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()

    ema_fast = EMAIndicator(df['close'], window=9)
    ema_slow = EMAIndicator(df['close'], window=21)
    df['ema_9'] = ema_fast.ema_indicator()
    df['ema_21'] = ema_slow.ema_indicator()

    rsi = RSIIndicator(df['close'], window=14)
    df['rsi'] = rsi.rsi()

    bb = BollingerBands(df['close'])
    df['bb_upper'] = bb.bollinger_hband()
    df['bb_lower'] = bb.bollinger_lband()

    # === Latest candle data ===
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    score = 0
    reasons = []

    # === Logic ===

    # MACD Bullish
    if latest['macd'] > latest['macd_signal']:
        score += 1
        reasons.append("MACD Bullish")
    elif latest['macd'] < latest['macd_signal']:
        score -= 1
        reasons.append("MACD Bearish")

    # EMA Crossover
    if latest['ema_9'] > latest['ema_21']:
        score += 1
        reasons.append("EMA Bullish")
    elif latest['ema_9'] < latest['ema_21']:
        score -= 1
        reasons.append("EMA Bearish")

    # RSI
    if latest['rsi'] < 30:
        score += 1
        reasons.append("RSI Oversold")
    elif latest['rsi'] > 70:
        score -= 1
        reasons.append("RSI Overbought")

    # Bollinger Band
    if latest['close'] < latest['bb_lower']:
        score += 1
        reasons.append("Close below BB lower")
    elif latest['close'] > latest['bb_upper']:
        score -= 1
        reasons.append("Close above BB upper")

    # === Final Decision ===
    direction = None
    confidence = abs(score) * 20  # Max 80%
    reason_str = ", ".join(reasons)

    if score >= 2:
        direction = "BUY"
    elif score <= -2:
        direction = "SELL"

    return direction, confidence, reason_str
