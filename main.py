import telebot
import os
from flask import Flask
from threading import Thread

# --- KONFIGURIMI FINAL DHE I SIGURT ---
TOKEN = "8728522462:AAFCmo5DFol1wzr23sFvZOt--IUx9aukgoU"
# ID-ja jote e saktë për kontrollin e sistemit
ADMIN_ID = 7954635482 

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    # Pergjigje minimale per te shmangur "Output too large" ne Cron-job
    return "OK"

def run():
    # Perdorum porten 8080 qe eshte me e qendrueshme ne Render
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID)
@bot.message_handler(commands=['start', 'snipe'])
def handle_admin(message):
    bot.reply_to(message, f"👿 Sistemi Sniper u lidh me ID-në tënde: {ADMIN_ID}\n\nStatusi: ONLINE 24/7 dhe gati për gjueti!")

if __name__ == "__main__":
    keep_alive()
    print("🤖 Bot is starting...")
    # non_stop=True siguron qe boti te mos fiket nga gabimet e rrjetit
    bot.infinity_polling(non_stop=True)
