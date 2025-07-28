from pocket_bot import start_pocket_bot
from telegram_bot import run_telegram_bot_background
import threading
import time

if __name__ == "__main__":
    print("📦 Starting Pocket Option Signal Bot (Telegram Only)...")

    # Start signal bot
    threading.Thread(target=start_pocket_bot, daemon=True).start()

    # Start Telegram bot
    threading.Thread(target=run_telegram_bot_background, daemon=True).start()

    # Keep alive
    while True:
        time.sleep(60)
