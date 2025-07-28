# main.py

import threading
from pocket_bot import start_pocket_bot
from telegram_bot import run_telegram_bot_background

if __name__ == "__main__":
    print("📦 Starting Pocket Option Bot System...")

    # Start the Pocket Option bot in a background thread
    threading.Thread(target=start_pocket_bot, daemon=True).start()

    # Start the Telegram bot in a background thread
    threading.Thread(target=run_telegram_bot_background, daemon=True).start()

    # Keep the main thread alive
    while True:
        pass
