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
    df['macd_hist'] = macd.macd_diff()

    ema_fast = EMAIndicator(df['close'], window=9)
    ema_slow = EMAIndicator(df['close'], window=21)
    df['ema_9'] = ema_fast.ema_indicator()
    df['ema_21'] = ema_slow.ema_indicator()

    rsi = RSIIndicator(df['close'], window=14)
    df['rsi'] = rsi.rsi()

    bb = BollingerBands(df['close'])
    df['bb_upper'] = bb.bollinger_hband()
    df['bb_lower'] = bb.bollinger_lband()
    df['bb_middle'] = bb.bollinger_mavg()

    # === Latest candle data ===
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    score = 0
    reasons = []

    # === Looser Logic ===

    # MACD
    if latest['macd'] > latest['macd_signal']:
        score += 1
        reasons.append("MACD Bullish")
    elif latest['macd'] < latest['macd_signal']:
        score -= 1
        reasons.append("MACD Bearish")

    # EMA
    if latest['ema_9'] > latest['ema_21']:
        score += 1
        reasons.append("EMA Bullish")
    elif latest['ema_9'] < latest['ema_21']:
        score -= 1
        reasons.append("EMA Bearish")

    # RSI (relaxed)
    if latest['rsi'] < 40:
        score += 1
        reasons.append("RSI Slightly Oversold")
    elif latest['rsi'] > 60:
        score -= 1
        reasons.append("RSI Slightly Overbought")

    # Bollinger Band + middle band
    if latest['close'] < latest['bb_lower']:
        score += 1
        reasons.append("Close near BB lower")
    elif latest['close'] > latest['bb_upper']:
        score -= 1
        reasons.append("Close near BB upper")
    elif latest['close'] < latest['bb_middle']:
        score += 0.5
        reasons.append("Close below BB mid")
    elif latest['close'] > latest['bb_middle']:
        score -= 0.5
        reasons.append("Close above BB mid")

    # === Final Decision ===
    direction = None
    confidence = min(abs(score) * 20, 100)
    reason_str = ", ".join(reasons)

    # 🟢 Trigger signals even with score = ±0.5
    if score > 0:
        direction = "BUY"
    elif score < 0:
        direction = "SELL"

    return direction, int(confidence), reason_str
