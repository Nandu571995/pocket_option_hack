import os
import json
import datetime
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN") or "8330981377:AAH3GUheRzKgpd4NDx0cIIGo4FVs1PDMyTA"
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") or "1014815784"

bot = Bot(token=TELEGRAM_TOKEN)

def send_signal_telegram(signal):
    message = (
        f"📢 {signal['timeframe']} Signal Alert!\n"
        f"🪙 Asset: {signal['asset']}\n"
        f"🎯 Direction: {signal['direction']}\n"
        f"🧠 Confidence: {signal['confidence']}%\n"
        f"📊 Reason: {signal['reason']}\n"
        f"🕒 Time: {signal['timestamp']}"
    )
    bot.send_message(chat_id=CHAT_ID, text=message)

def send_performance_report():
    try:
        with open("signals.json", "r") as f:
            data = json.load(f)
        now = datetime.datetime.now()
        report = "📊 Signal Accuracy Report\n\n"
        for tf in data:
            signals = [s for s in data[tf] if 'result' in s]
            correct = sum(1 for s in signals if s['result'] == "✅")
            total = len(signals)
            accuracy = int((correct / total) * 100) if total > 0 else 0
            report += f"{tf}: {correct}/{total} ✅ ({accuracy}%)\n"
        bot.send_message(chat_id=CHAT_ID, text=report)
    except Exception as e:
        bot.send_message(chat_id=CHAT_ID, text="Error in generating report")

def start(update: Update, context: CallbackContext):
    update.message.reply_text("✅ Bot is running. Use /performance to get stats.")

def performance(update: Update, context: CallbackContext):
    send_performance_report()

def run_telegram_bot_background():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("performance", performance))
    updater.start_polling()