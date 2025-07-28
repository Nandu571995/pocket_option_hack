import time
import json
import datetime
from strategy import generate_signal
from telegram_bot import send_signal_telegram

ASSETS = ["EUR/USD", "GBP/USD", "USD/JPY", "BTC/USD", "GOLD"]
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
    import random
    success = random.random() < 0.7
    signal['result'] = "✅" if success else "❌"
    return signal

def start_pocket_bot():
    print("🚀 Pocket Option Signal Bot Running...")
    while True:
        now = datetime.datetime.now()
        current_minute = now.minute
        current_second = now.second

        if current_second == 0 and current_minute % 1 == 0:
            signals = load_signals()
            timestamp = now.strftime("%H:%M")
            for tf in TIMEFRAMES:
                for asset in ASSETS:
                    direction, confidence, reason = generate_signal(asset, tf)
                    signal = {
                        "asset": asset,
                        "direction": direction,
                        "confidence": confidence,
                        "reason": reason,
                        "timeframe": tf,
                        "timestamp": f"{timestamp}–{(now + datetime.timedelta(minutes=1)).strftime('%H:%M')}"
                    }
                    signals[tf].append(validate_signal(signal))
                    send_signal_telegram(signal)
            save_signals(signals)
        time.sleep(1)