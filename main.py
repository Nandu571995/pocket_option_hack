import threading
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

from pocket_bot import start_pocket_bot
from telegram_bot import run_telegram_bot_background

def dummy_http_server():
    port = int(os.environ.get("PORT", 10000))  # This satisfies Render port binding
    with TCPServer(("0.0.0.0", port), SimpleHTTPRequestHandler) as httpd:
        print(f"🟢 Dummy server running on port {port}")
        httpd.serve_forever()

if __name__ == "__main__":
    print("📦 Starting Pocket Option Signal Bot (Telegram only)")

    # Run dummy HTTP server to satisfy Render Web Service
    threading.Thread(target=dummy_http_server, daemon=True).start()

    # Run trading signal bot
    threading.Thread(target=start_pocket_bot, daemon=True).start()

    # Run Telegram bot
    threading.Thread(target=run_telegram_bot_background, daemon=True).start()

    # Keep alive
    while True:
        pass
