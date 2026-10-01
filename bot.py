step']==1:
            data['c1']=cote; data['step']=data['dom'],data['ext']
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
