# telegram_bot.py

import os
import json
import time
from telegram import Bot

# Load environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("❌ TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set in environment variables.")
    raise Exception("Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in your Render environment.")

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
        print(f"Sending to Telegram: {message.replace(chr(10), '; ')}")
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode="Markdown")
        print("✅ Signal sent to Telegram:", signal['asset'], signal['timeframe'])
    except Exception as e:
        print("❌ Telegram send error:", str(e))

def send_test_message():
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="✅ Test message from Render deployment!", parse_mode="Markdown")
        print("✅ Test message sent. If you see this in Telegram, your bot is working!")
    except Exception as e:
        print("❌ Telegram test send error:", str(e))

def send_performance_summary(timeframe=None):
    try:
        with open("signals.json", "r") as f:
            data = json.load(f)
    except:
        print("⚠️ Could not load signals.json for summary.")
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
            print(f"Sending performance summary: {msg}")
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg, parse_mode="Markdown")
        except Exception as e:
            print("❌ Telegram summary send error:", str(e))

def run_telegram_bot_background():
    # Send a test message on start
    send_test_message()

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
