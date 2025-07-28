# strategy.py

import random

def generate_signal(asset, timeframe):
    """
    Simulates signal generation logic.
    You can plug in real indicators here later.
    """
    directions = ["BUY", "SELL"]
    direction = random.choice(directions)
    confidence = random.randint(70, 95)

    reasons = [
        "MACD crossover + RSI divergence",
        "EMA 20/50 crossover + Bollinger breakout",
        "Strong RSI + Momentum spike",
        "Price rejection + MACD alignment",
        "RSI oversold + Bullish engulfing"
    ]
    reason = random.choice(reasons)

    return direction, confidence, reason
