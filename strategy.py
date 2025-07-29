import pandas as pd
import numpy as np
from pocket_option_scraper import get_candles

def generate_signal(asset, timeframe):
    df = get_candles(asset, timeframe, limit=50)
    
    if df.empty or len(df) < 30:
        print(f"⚠️ Not enough data for {asset} {timeframe}")
        return "NO_SIGNAL", 0, "Not enough candles"

    try:
        df["close"] = pd.to_numeric(df["close"])
        df["ema9"] = df["close"].ewm(span=9).mean()
        df["ema21"] = df["close"].ewm(span=21).mean()
        df["macd"] = df["close"].ewm(span=12).mean() - df["close"].ewm(span=26).mean()
        df["signal"] = df["macd"].ewm(span=9).mean()
        df["rsi"] = compute_rsi(df["close"], 14)

        # Bollinger Bands
        df["sma20"] = df["close"].rolling(window=20).mean()
        df["stddev"] = df["close"].rolling(window=20).std()
        df["upper_band"] = df["sma20"] + 2 * df["stddev"]
        df["lower_band"] = df["sma20"] - 2 * df["stddev"]

        latest = df.iloc[-1]
        prev = df.iloc[-2]

        reasons = []

        # EMA Crossover
        if prev["ema9"] < prev["ema21"] and latest["ema9"] > latest["ema21"]:
            reasons.append("EMA9 crossed above EMA21")
        elif prev["ema9"] > prev["ema21"] and latest["ema9"] < latest["ema21"]:
            reasons.append("EMA9 crossed below EMA21")

        # MACD crossover
        if prev["macd"] < prev["signal"] and latest["macd"] > latest["signal"]:
            reasons.append("MACD bullish crossover")
        elif prev["macd"] > prev["signal"] and latest["macd"] < latest["signal"]:
            reasons.append("MACD bearish crossover")

        # RSI logic
        if latest["rsi"] < 30:
            reasons.append("RSI oversold")
        elif latest["rsi"] > 70:
            reasons.append("RSI overbought")

        # Bollinger Bounce
        if latest["close"] <= latest["lower_band"]:
            reasons.append("Price near lower Bollinger Band")
        elif latest["close"] >= latest["upper_band"]:
            reasons.append("Price near upper Bollinger Band")

        # Signal decision
        if "EMA9 crossed above EMA21" in reasons or "MACD bullish crossover" in reasons or "RSI oversold" in reasons:
            direction = "BUY"
        elif "EMA9 crossed below EMA21" in reasons or "MACD bearish crossover" in reasons or "RSI overbought" in reasons:
            direction = "SELL"
        else:
            print(f"⏭️ Skipped {asset} {timeframe} — No valid technical signal")
            return "NO_SIGNAL", 0, "No valid technical signal"

        confidence = min(100, 50 + 10 * len(reasons))
        reason_text = ", ".join(reasons)

        print(f"✅ Signal generated for {asset} {timeframe}: {direction} ({confidence}%) — {reason_text}")
        return direction, confidence, reason_text

    except Exception as e:
        print(f"❌ Strategy error for {asset} {timeframe}: {e}")
        return "NO_SIGNAL", 0, str(e)

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
