from telegram import Bot

TOKEN = "8330981377:AAH3GUheRzKgpd4NDx0cIIGo4FVs1PDMyTA"
CHAT_ID = "1014815784"

bot = Bot(token=TOKEN)
bot.send_message(chat_id=CHAT_ID, text="✅ Test message from bot!")
