import telebot
import os
from flask import Flask
from threading import Thread

# --- KONFIGURIMI I BLINDUAR ---
TOKEN = "8728522462:AAFCmo5DFol1wzr23sFvZOt--IUx9aukgoU"
bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Sniper is Awake!"

def run():
    # RREGULLIMI I PORTES: Render kerkon PORT 10000 automatikisht
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

@bot.message_handler(commands=['start', 'snipe'])
def welcome(message):
    bot.reply_to(message, "👿 Sistemi Sniper u aktivizua dhe është i pandalshëm!")

if __name__ == "__main__":
    keep_alive()
    print("🤖 Bot is starting...")
    # Shtohet non_stop=True per stabilitet ne servera falas
    bot.infinity_polling(non_stop=True)
