
import os
import telebot
from flask import Flask
import threading

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "MT05 BOT Live! 🔥"

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🔥 MT05 BOT prêt boss!\nEnvoie: Real vs Barca")

@bot.message_handler(func=lambda m: True)
def analyze(m):
    txt = m.text
    if "vs" not in txt.lower():
        bot.send_message(m.chat.id, "Format: Real vs Barca")
        return
    t1, t2 = txt.split("vs",1)
    res = f"⚽ MT05: {t1.strip().upper()} vs {t2.strip().upper()}\n\n🎯 Score: 3-2 (22%)\n2-4 (18%)\n3-4 (15%)\n\n💡 Conseil: 1X X2  +7.5) Under 3.5"
    bot.send_message(m.chat.id, res)

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="4.5.3.05", port=int(os.environ.get("PORT",10000)))
