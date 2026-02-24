import telebot
import os
from flask import Flask
from threading import Thread

# --- KONFIGURIMI I PASTËR ---
TOKEN = "8728522462:AAFCmo5DFol1wzr23sFvZOt--IUx9aukgoU"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    # Kjo pergjigje e shkurter zgjidh problemin "Output too large"
    return "OK"

def run():
    # Render kerkon PORT 10000
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

@bot.message_handler(commands=['start', 'snipe'])
def welcome(message):
    bot.reply_to(message, "👿 Sistemi Sniper është LIVE dhe i heshtur!")

if __name__ == "__main__":
    keep_alive()
    # non_stop=True ben qe boti te mos fiket nese ka nje gabim te vogel rrjeti
    bot.infinity_polling(non_stop=True)
