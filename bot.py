
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
def analyze(message):
    if "vs" not in message.text.lower() and "contre" not in message.text.lower():
        bot.send_message(message.chat.id, "Envoie: Real vs Barca")
        return
    txt = message.text.lower().replace("contre","vs")
    team1, team2 = txt.split("vs",1)
    result = f"⚽ MT05: {team1.strip().upper()} vs {team2.strip().upper()}\n\n🎯 Scores probables:\n1-1 (22% ⭐)\n2-1 (18%)\n1-0 (15%)\n\n💡 Conseil: 1X + Under 3.5 - 78% confiance"
    bot.send_message(message.chat.id, result)

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
