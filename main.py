import telebot
import os
from flask import Flask
from threading import Thread

# --- KONFIGURIMI ---
TOKEN = "8728522462:AAFCmo5DFol1wzr23sFvZOt--IUx9aukgoU"
bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Sniper is Awake!"

def run():
    # Render kerkon porten 10000 ose 8080
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

@bot.message_handler(commands=['start', 'snipe'])
def welcome(message):
    bot.reply_to(message, "👿 Sistemi Sniper është ONLINE 24/7!\n\nDuke skanuar rrjetin për mbetje dhe arbitrazh...")

if __name__ == "__main__":
    keep_alive() # Nis serverin web per Cron-job
    bot.infinity_polling()
