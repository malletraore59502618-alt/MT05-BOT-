import telebot
BOT_TOKEN = "8802330817:AAEzZmozKOx_Cvlc_hC8-AVJaLkCRxzMibk"
bot = telebot.TeleBot(BOT_TOKEN)
users = {}
@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "MT05 PRO MAX EN LIGNE\nEnvoie: Domicile vs Exterieur")
@bot.message_handler(func=lambda m: 'vs' in m.text.lower() and '/' not in m.text)
def vs_handler(m):
    parts=m.text.lower().split('vs')
    dom=parts[0].strip().title()
    ext=parts[1].strip().title()
    users[m.chat.id]={'dom':dom,'ext':ext,'s_to(m, f"Match: {dom} vs {ext}\nCote DOMICILE 1?")
@bot.message_handler(func=lambda m: True)
def cotes(m):
    cid=m.chat.id
    if cid not in users: return
    data=users[cid]
    try:
        cote=float(m.text.replace(',', '.'))
        if data['step']==1:
            data['c1']=cote; data['step']=2
            bot.reply_to(m, "Cote NUL X?")
        elif data['step']==2:
            data['cx']=cote; data['step']=3
            bot.reply_to(m, "Cote EXTERIEUR 2?")
        elif data['step']==3:
            data['c2']=cote
            dom,ext=data['dom'],data['ext']
            c1,cx,c2=data['c1'],data['cx'],data['c2']
            if c1<1.85: pron=f"Victoire {dom} + -4.5 buts"
            elif c2<1.85: pron=f"Victoire {ext} + -4.5 buts"
            elif cx<3.1: pron="NUL ou 1X - Under 3.5"
            else: pron=f"1X - {dom} ne perd pas"
            bot.reply_to(m, f"MT05 ANALYSE\n{dom} vs {ext}\n{c1}/{cx}/{c2}\nPRONO: {pron}")
            del users[cid]
    except: bot.reply_to(m, "Envoie nombre ex: 2.10")
print("MT05 PRO MAX en marche...")
bot.infinity_polling()
