import threading
from pocket_bot import start_pocket_bot
from telegram_bot import run_telegram_bot_background

if __name__ == "__main__":
    print("📦 Starting Pocket Option Bot System (Telegram only)...")
    threading.Thread(target=start_pocket_bot, daemon=True).start()
    threading.Thread(target=run_telegram_bot_background, daemon=True).start()
    while True:
        pass