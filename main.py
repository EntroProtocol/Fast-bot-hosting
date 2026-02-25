import telebot
import requests
import os
from flask import Flask
from threading import Thread

TOKEN = "8728522462:AAFCmo5DFol1wzr23sFvZOt--IUx9aukgoU"
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

@app.route('/')
def home():
    return "LUIS ELITE ONLINE", 200

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

@bot.message_handler(commands=['scan'])
def handle_scan(message):
    try:
        addr = message.text.split()[1]
        res = requests.get(f"https://api.dexscreener.com/latest/dex/tokens/{addr}").json()
        data = res['pairs'][0]
        
        report = (
            f"🛡️ LUIS ELITE | SUPREME AUDIT 🛡️\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 Developer: Luis Elite\n"
            f"💎 TOKEN: {data['baseToken']['name']}\n"
            f"💰 Price: ${data['priceUsd']}\n"
            f"🌊 Liquidity: ${data['liquidity']['usd']}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📢 JOIN: https://t.me/+i2qqsRxByfE0NWE0"
        )
        bot.reply_to(message, report)
    except:
        bot.reply_to(message, "❌ Error: Kontrata nuk u gjet.")

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling(skip_pending=True)
