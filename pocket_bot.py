# pocket_bot.py

import time
import json
import datetime
from strategy import generate_signal
from telegram_bot import send_signal_telegram

# ✅ FULL asset list (OTC + currency)
ASSETS = [
    "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD",
    "NZD/USD", "USD/CHF", "EUR/GBP", "EUR/JPY", "BTC/USD", "ETH/USD",
    "GOLD", "SILVER", "LTC/USD", "OTC_EUR/USD", "OTC_GBP/USD", "OTC_USD/JPY"
]

TIMEFRAMES = ["1m", "3m", "5m", "10m"]

def load_signals():
    try:
        with open("signals.json", "r") as f:
            return json.load(f)
    except:
        return {tf: [] for tf in TIMEFRAMES}

def save_signals(data):
    with open("signals.json", "w") as f:
        json.dump(data, f, indent=2)

def validate_signal(signal):
    # Dummy validation for now (replace with actual logic later)
    import random
    success = random.random() < 0.7
    signal['result'] = "✅" if success else "❌"
    return signal

def start_pocket_bot():
    print("🚀 Pocket Option Signal Bot Running...")
    signals = load_signals()

    while True:
        now = datetime.datetime.now()
        seconds = now.second

        # Trigger 30–60 seconds before the candle starts
        if 0 <= seconds <= 5:
            timestamp = now.strftime("%H:%M")
            next_min = (now + datetime.timedelta(minutes=1)).strftime('%H:%M')

            for tf in TIMEFRAMES:
                for asset in ASSETS:
                    direction, confidence, reason = generate_signal(asset, tf)

                    if direction in ["BUY", "SELL"]:
                        signal = {
                            "asset": asset,
                            "direction": direction,
                            "confidence": confidence,
                            "reason": reason,
                            "timeframe": tf,
                            "timestamp": f"{timestamp}–{next_min}"
                        }
                        signal = validate_signal(signal)
                        signals[tf].append(signal)
                        send_signal_telegram(signal)

            save_signals(signals)
            time.sleep(60)  # avoid double execution

        time.sleep(1)
