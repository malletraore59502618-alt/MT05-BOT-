import os
import telebot
from flask import Flask
import threading
import random

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Garde Render vivant
@app.route('/')
def home():
    return "MT05 BOT ULTRA LIVE"

# --- LOGIQUE PRONO ---
def generer_analyse(match_text):
    # Ex: CITY vs PARIS
    parts = match_text.lower().split("vs")
    if len(parts) < 2:
        domicile = "Domicile"
        exterieur = "Extérieur"
    else:
        domicile = parts[0].strip().upper()
        exterieur = parts[1].strip().upper()

    # Simule tes % (tu pourras brancher ton IA après)
    scores = [
        ("1-1", 22),
        ("2-1", 18),
        ("1-0", 15),
        ("0-1", 12),
        ("2-0", 10)
    ]
    random.shuffle(scores)

    # Calcul victoire
    victoire_dom = random.randint(45, 58)
    victoire_ext = random.randint(20, 35)
    nul = 100 - victoire_dom - victoire_ext

    msg = f"""
🔥 **MT05 ULTRA ANALYSE** 🔥
⚔️ {domicile} vs {exterieur}

🎯 **SCORES EXACTS PROBABLES :**
🥇 {scores[0][0]} - {scores[0][1]}%
🥈 {scores[1][0]} - {scores[1][1]}%
🥉 {scores[2][0]} - {scores[2][1]}%

📊 **ISSUE DU MATCH :**
🏠 Victoire {domicile}: {victoire_dom}%
🤝 Nul: {nul}%
✈️ Victoire {exterieur}: {victoire_ext}%

💡 **CONSEIL MT05 :**
{"✅ 1X + Under 3.5" if victoire_dom > victoire_ext else "✅ X2 + Under 3.5"} - SAFE
🔥 Score le plus sûr: {scores[0][0]}

👇 Prono VIP complet?
"""
    return msg

# --- BOUTONS ---
@bot.message_handler(commands=['start'])
def start(m):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🔍 ANALYSER UN MATCH", callback_data="analyser"))
    markup.add(telebot.types.InlineKeyboardButton("💎 CANAL VIP", url="https://t.me/MT05Officiel")) # CHANGE TON LIEN ICI
    bot.send_message(m.chat.id,
        "Bienvenue sur **MT05 BOT ULTRA** 🤖\n\nClique sur ANALYSER et envoie un match comme:\n`CITY vs PARIS`",
        reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "analyser")
def ask_match(call):
    bot.send_message(call.message.chat.id, "Envoie le match maintenant:\nEx: `CITY vs PARIS BUT PLUS`")

@bot.message_handler(func=lambda m: "vs" in m.text.lower())
def analyse_auto(m):
    analyse = generer_analyse(m.text)
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🔄 Re-analyser", callback_data="analyser"))
    bot.send_message(m.chat.id, analyse, reply_markup=markup, parse_mode="Markdown")

# --- LANCEMENT ---
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
