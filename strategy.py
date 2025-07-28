# strategy.py
import random

def generate_signal(asset, timeframe):
    # Simulate real indicator-based decision-making
    indicators = []

    # Strategy placeholder logic (to be replaced by real data scraping if Pocket Option gives it)
    macd = random.choice([True, False])
    ema = random.choice([True, False])
    rsi = random.choice([True, False])
    bb = random.choice([True, False])

    if macd: indicators.append("MACD crossover")
    if ema: indicators.append("EMA trend")
    if rsi: indicators.append("RSI overbought/oversold")
    if bb: indicators.append("Bollinger Band squeeze")

    direction = "GREEN" if macd or ema else "RED"
    confidence = round((macd + ema + rsi + bb) / 4 * 100)
    reason = " + ".join(indicators) or "Low confidence signal"

    return direction, confidence, reason
