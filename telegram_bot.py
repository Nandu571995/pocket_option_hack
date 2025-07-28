# telegram_bot.py

import os
import json
import time
from telegram import Bot

# Load environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or "8330981377:AAH3GUheRzKgpd4NDx0cIIGo4FVs1PDMyTA"
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") or "1014815784"

# Initialize bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

def send_signal_telegram(signal):
    try:
        message = (
            f"📡 *Signal Alert* ({signal['timeframe']})\n"
            f"🔹 *Asset:* {signal['asset']}\n"
            f"📈 *Direction:* {signal['direction']}\n"
            f"🎯 *Time:* {signal['timestamp']}\n"
            f"💬 *Reason:* {signal['reason']}\n"
            f"📊 *Confidence:* {signal['confidence']}%"
        )
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode="Markdown")
        print("✅ Signal sent to Telegram:", signal['asset'], signal['timeframe'])
    except Exception as e:
        print("❌ Telegram send error:", str(e))

def send_performance_summary(timeframe=None):
    try:
        with open("signals.json", "r") as f:
            data = json.load(f)
    except:
        return

    summary = []
    total = 0
    success = 0

    if timeframe:
        signals = data.get(timeframe, [])
        for sig in signals:
            if 'result' in sig:
                total += 1
                if sig['result'] == "✅":
                    success += 1
        if total > 0:
            accuracy = round((success / total) * 100, 2)
            summary.append(f"{timeframe.upper()} Accuracy: {success}/{total} = {accuracy}%")
    else:
        for tf, signals in data.items():
            tf_total = tf_success = 0
            for sig in signals:
                if 'result' in sig:
                    tf_total += 1
                    if sig['result'] == "✅":
                        tf_success += 1
            if tf_total > 0:
                accuracy = round((tf_success / tf_total) * 100, 2)
                summary.append(f"{tf.upper()}: {tf_success}/{tf_total} ✅ = {accuracy}%")

    if summary:
        msg = "📊 *Performance Summary*\n" + "\n".join(summary)
        try:
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg, parse_mode="Markdown")
        except Exception as e:
            print("❌ Telegram summary send error:", str(e))

def run_telegram_bot_background():
    while True:
        now = time.localtime()
        # Send hourly stats at HH:59
        if now.tm_min == 59 and now.tm_sec == 0:
            send_performance_summary()
            time.sleep(60)
        # Send daily stats at 23:59
        if now.tm_hour == 23 and now.tm_min == 59 and now.tm_sec == 30:
            send_performance_summary()
            time.sleep(60)
        time.sleep(1)
