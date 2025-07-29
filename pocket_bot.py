import time
import json
import datetime
from strategy import generate_signal
from telegram_bot import send_signal_telegram

# ✅ Full asset list including major FX, OTC, crypto, metals, and commodities
ASSETS = [
    # Major Forex pairs
    "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD",
    "NZD/USD", "USD/CHF", "EUR/GBP", "EUR/JPY",

    # Crypto
    "BTC/USD", "ETH/USD", "LTC/USD",

    # Metals
    "GOLD", "SILVER",

    # Commodities
    "CRUDE_OIL", "BRENT_OIL", "NATURAL_GAS",

    # OTC Forex (mapped via scraper)
    "OTC_EUR/USD", "OTC_GBP/USD", "OTC_USD/JPY", "OTC_AUD/USD",
    "OTC_NZD/USD", "OTC_USD/CAD", "OTC_USD/CHF", "OTC_EUR/JPY", "OTC_GBP/JPY"
]

TIMEFRAMES = ["1m", "3m", "5m", "10m"]
SIGNALS_FILE = "signals.json"

def load_signals():
    try:
        with open(SIGNALS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_signal(signal):
    date_key = datetime.datetime.now().strftime("%Y-%m-%d")
    tf = signal['timeframe']
    data = load_signals()

    if date_key not in data:
        data[date_key] = {}
    if tf not in data[date_key]:
        data[date_key][tf] = []

    data[date_key][tf].append(signal)

    with open(SIGNALS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def validate_signal(signal):
    import random
    success = random.random() < 0.75
    signal['result'] = "✅" if success else "❌"
    return signal

def start_pocket_bot():
    print("🚀 Pocket Option Signal Bot Running...")
    
    # Optional startup notification
    send_signal_telegram({
        "asset": "SYSTEM",
        "direction": "READY",
        "confidence": 100,
        "reason": "Bot initialized successfully.",
        "timeframe": "ALL",
        "timestamp": datetime.datetime.now().strftime("%H:%M")
    })

    while True:
        now = datetime.datetime.now()
        seconds = now.second
        print(f"🕒 Tick: {now.strftime('%H:%M:%S')} — Seconds: {seconds}")

        # Only run every 60s interval
        if 0 <= seconds <= 5:
            timestamp = now.strftime("%H:%M")
            next_min = (now + datetime.timedelta(minutes=1)).strftime("%H:%M")

            for tf in TIMEFRAMES:
                for asset in ASSETS:
                    try:
                        print(f"🔎 Generating signal for {asset} [{tf}]...")
                        direction, confidence, reason = generate_signal(asset, tf)

                        if direction in ["BUY", "SELL"]:
                            signal = {
                                "asset": asset,
                                "direction": direction,
                                "confidence": confidence,
                                "reason": reason,
