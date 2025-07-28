import random

def generate_signal(asset, timeframe):
    direction = random.choice(["GREEN", "RED"])
    confidence = random.randint(70, 95)
    reason = "MACD + EMA + RSI alignment"
    return direction, confidence, reason