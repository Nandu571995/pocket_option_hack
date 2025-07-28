# strategy.py

import ta
import pandas as pd

def generate_signal(df, timeframe):
    df = df.copy()
    if len(df) < 50:
        return None

    # Indicators
    df["EMA20"] = ta.trend.ema_indicator(df["close"], window=20)
    df["EMA50"] = ta.trend.ema_indicator(df["close"], window=50)
    macd = ta.trend.macd(df["close"])
    df["MACD"] = macd.macd()
    df["MACD_signal"] = macd.macd_signal()
    df["RSI"] = ta.momentum.rsi(df["close"], window=14)
    bb = ta.volatility.BollingerBands(df["close"])
    df["BB_upper"] = bb.bollinger_hband()
    df["BB_lower"] = bb.bollinger_lband()

    latest = df.iloc[-1]
    previous = df.iloc[-2]

    signal = None
    reason = []

    # ✅ More lenient MACD crossover
    if previous["MACD"] < previous["MACD_signal"] and latest["MACD"] > latest["MACD_signal"]:
        reason.append("MACD Bullish crossover")
        signal = "BUY"
    elif previous["MACD"] > previous["MACD_signal"] and latest["MACD"] < latest["MACD_signal"]:
        reason.append("MACD Bearish crossover")
        signal = "SELL"

    # ✅ Reduced EMA crossover threshold
    if latest["EMA20"] > latest["EMA50"] * 0.995:
        if signal == "BUY":
            reason.append("EMA20 > EMA50 (mild)")
        elif not signal:
            signal = "BUY"
            reason.append("EMA20 > EMA50")
    elif latest["EMA20"] < latest["EMA50"] * 1.005:
        if signal == "SELL":
            reason.append("EMA20 < EMA50 (mild)")
        elif not signal:
            signal = "SELL"
            reason.append("EMA20 < EMA50")

    # ✅ Wider RSI zone
    if latest["RSI"] < 40:
        if signal == "BUY":
            reason.append("RSI Oversold (<40)")
        elif not signal:
            signal = "BUY"
            reason.append("RSI Oversold")
    elif latest["RSI"] > 60:
        if signal == "SELL":
            reason.append("RSI Overbought (>60)")
        elif not signal:
            signal = "SELL"
            reason.append("RSI Overbought")

    # ✅ Bollinger Band near touch instead of strict
    if latest["close"] <= latest["BB_lower"] * 1.01:
        if signal == "BUY":
            reason.append("Near Lower BB")
        elif not signal:
            signal = "BUY"
            reason.append("Near Lower BB")
    elif latest["close"] >= latest["BB_upper"] * 0.99:
        if signal == "SELL":
            reason.append("Near Upper BB")
        elif not signal:
            signal = "SELL"
            reason.append("Near Upper BB")

    # ✅ Confidence Score
    confidence = int(len(reason) * 15 + (5 if signal else 0))
    if confidence > 99:
        confidence = 99

    if signal:
        return {
            "direction": signal,
            "reason": " + ".join(reason),
            "confidence": confidence
        }

    return None
