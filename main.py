import telebot
import requests
import os
from flask import Flask
from threading import Thread

# --- IDENTITY ---
TOKEN = "8728522462:AAFCmo5DFol1wzr23sFvZOt--IUx9aukgoU"
ADMIN_ID = 7954635482 
GROUP_LINK = "https://t.me/+i2qqsRxByfE0NWE0"
BRAND_NAME = "LUIS ELITE"

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

@app.route('/')
def home():
    return "LUIS ELITE ENGINE: ONLINE", 200

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# --- MODERATION & SCAN ---
@bot.message_handler(func=lambda m: True)
def handle_messages(message):
    if message.text:
        # 1. Anti-Toxic Filter
        if message.from_user.id != ADMIN_ID:
            if any(word in message.text.lower() for word in ["scam", "fuck", "rug"]):
                bot.delete_message(message.chat.id, message.message_id)
                return

        # 2. Scan Command
        if message.text.startswith('/scan'):
            try:
                addr = message.text.split()[1]
                res = requests.get(f"https://api.dexscreener.com/latest/dex/tokens/{addr}").json()
                data = res['pairs'][0]
                
                liq = float(data.get('liquidity', {}).get('usd', 0))
                mcap = float(data.get('fdv', 0))
                status = "🟢 VERIFIED REAL" if liq > 20000 else "🔴 HIGH RISK"

                report = (
                    f"🛡️ {BRAND_NAME} | SUPREME AUDIT 🛡️\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"👤 Developer: Luis Elite\n"
                    f"💎 TOKEN: {data['baseToken']['name']}\n"
                    f"📍 Contract: {addr}\n\n"
                    f"💰 Price: ${data['priceUsd']}\n"
                    f"💵 MCap: ${mcap:,.0f}\n"
                    f"🌊 Liquidity: ${liq:,.2f}\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"🕵️ Status: {status}\n"
                    f"🔥 Statusi: LIVE DATA\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"📢 JOIN: {GROUP_LINK}"
                )
                bot.reply_to(message, report)
            except:
                bot.reply_to(message, "❌ Adresa nuk u gjet.")

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling(skip_pending=True)
