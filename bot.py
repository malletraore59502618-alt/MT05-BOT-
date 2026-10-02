
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "TON_TOKEN_ICI"
CODE_PROMO = "7K9P2"
WAVE = "0701980963"
LIEN_VIP = "https://t.me/mt05_vip_ci"

def analyse_virtual(dom, ext):
    # Stats basées sur tes vrais coupons 4:2, 3:1, 1:2, 0:2
    return {
        "scores": [
            ("2-1", 18, "8.5"),
            ("1-2", 16, "9.2"),
            ("3-1", 14, "12.0"),   # Ton Arsenal 3-1
            ("2-2", 12, "13.5"),
            ("4-2", 10, "18.0"),   # Ton Portugal 4-2
            ("3-2", 8, "22.0"),
            ("0-2", 7, "15.0"),    # Ton River 0-2
            ("1-3", 5, "28.0"),
            ("3-4", 4, "45.0"),    # Ce que tu voulais
            ("4-3", 3, "50.0"),
            ("5-4", 2, "85.0"),
            ("4-5", 1, "95.0"),
        ],
        "pct_dom": 38, "pct_nul": 22, "pct_ext": 40,
        "safe": "Plus de 2.5 + Les Deux Marques (BTTS)"
    }

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = f"🔥 **MT05 V5 VIRTUAL EDITION** 🔥\n\n🎁 Code: `{CODE_PROMO}` | Wave: `{WAVE}`\n\n**Tape:**\n/fifa FRANCE vs ESPAGNE\n/fifa PORTUGAL vs FRANCE\n/vip - Pronos du jour\n\nJe donne 12 scores dont 4-2, 3-4, 5-4 ✅"
    await update.message.reply_text(msg, parse_mode='Markdown')

async def fifa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚽ Envoie: `PORTUGAL vs FRANCE` ou `RIVER vs COLO`", parse_mode='Markdown')

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    clean = re.sub(r'\d+[:]\d+', '', text)
    clean = re.sub(r'\d+\.\d+', '', clean)
    if 'vs' not in clean.lower(): return
    dom, ext = [x.strip().upper() for x in re.split(r'\s*vs\s*', clean, flags=re.I)]

    data = analyse_virtual(dom, ext)
    
    txt = f"🔥 **MT05 VIRTUAL ANALYSE** 🔥\n⚔️ **{dom} vs {ext}**\n\n"
    txt += f"🎯 **12 SCORES EXACTS VIRTUAL:**\n"
    for score, pct, cote in data["scores"]:
        emoji = "🔥" if pct >= 14 else "💰" if pct <= 5 else "•"
        txt += f"{emoji} {score} - {pct}% (cote {cote})\n"
    
    txt += f"\n📊 **CHANCES:**\n🏠 {dom} {data['pct_dom']}% | 🤝 Nul {data['pct_nul']}% | ✈️ {ext} {data['pct_ext']}%\n\n"
    txt += f"🔒 **SAFE VIRTUAL:**\n{data['safe']}\n✅ Comme ton coupon Arsenal 3-1 Plus de 3\n\n"
    txt += f"⚠️ **GROS COTES FUN:**\n3-4, 4-5, 5-4 → petite mise 100F seulement!"

    kb = [[InlineKeyboardButton("💎 REJOINDRE VIP - 2000F", url=LIEN_VIP)]]
    await update.message.reply_text(txt, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("fifa", fifa))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.run_polling()
