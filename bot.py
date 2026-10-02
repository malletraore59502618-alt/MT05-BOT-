
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# TON LIEN VIP - CHANGE ICI 👇
LIEN_VIP = "https://t.me/mt05_vip_ci" # Mets ton vrai t.me ici

def parse_match(text):
    # Cherche les cotes
    odds = re.findall(r'\d+\.\d+', text)
    odd_dom = float(odds[0]) if len(odds) > 0 else 2.0
    odd_ext = float(odds[1]) if len(odds) > 1 else 2.0

    # Nettoie le texte pour avoir que les noms d'équipe
    clean = re.sub(r'\d+\.\d+', '', text)
    clean = re.sub(r'\s+', ' ', clean).strip()

    if 'vs' in clean.lower():
        parts = re.split(r'\s*vs\s*', clean, flags=re.IGNORECASE)
        dom = parts[0].strip().upper()
        ext = parts[1].strip().upper()
        return dom, ext, odd_dom, odd_ext
    return None, None, 0, 0

def analyse_scores(odd_dom, odd_ext):
    # Logique MT05 ULTRA
    if odd_dom < odd_ext:
        return [
            ("1-1", 22),
            ("2-1", 18),
            ("1-0", 15),
            ("0-1", 12)
        ], 52, 22, 26
    else:
        return [
            ("1-3",2-3",3-4 50),
            ("2-1", 4-3",3-5",35),
            ("1-2",4-5",16),
            ("3-2",5-4",5-3",25)
        ], 26, 22, 52

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 **MT05 PRO MAX - BOT ULTRA** 🔥\n\n"
        "Envoie ton match comme ça :\n"
        "`Domicile vs Exterieur `\n"
        "ou\n"
        "`REAL 2.10 vs 3.20 BARCA`\n\n"
        "Je te donne Score Exact + Victoire % + SAFE",
        parse_mode='Markdown'
    )

async def handle_match(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    dom, ext, odd_dom, odd_ext = parse_match(text)

    if not dom:
        await update.message.reply_text("❌ Format invalide. Envoie : `Domicile vs Exterieur `", parse_mode='Markdown')
        return

    scores, pct_dom, pct_nul, pct_ext = analyse_scores(odd_dom, odd_ext)

    message = f"🔥 **MT05 ULTRA ANALYSE** 🔥\n"
    message += f"⚔️ **{dom} vs {ext}**\n\n"
    message += f"🎯 **SCORES EXACTS :**\n"
    for score, pct in scores:
        message += f"• {score} - {pct}%\n"
    message += f"\n📊 **ISSUE DU MATCH :**\n"
    message += f"🏠 Victoire {dom}: {pct_dom}%\n"
    message += f"🤝 Nul: {pct_nul}%\n"
    message += f"✈️ Victoire {ext}: {pct_ext}%\n\n"
    message += f"🔒 **SAFE :** 1X + Under 3.5" if pct_dom > pct_ext else f"🔒 **SAFE :** X2 +Plus 7.5 Under 3.5"

    keyboard = [[InlineKeyboardButton("💎 REJOINDRE VIP PRO", url=LIEN_VIP)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')

# LANCEUR
app = Application.builder().token("TON_TOKEN_8802330817:AAEzZmozKOx_Cvlc_hC8-AVJaLkCRxzMibk").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_match))
app.run_polling()
