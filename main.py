import telebot
import os
from flask import Flask
from threading import Thread

# --- KONFIGURIMI ---
TOKEN = "8728522462:AAFCmo5DFol1wzr23sFvZOt--IUx9aukgoU"
ADMIN_ID = 7954635482 

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

@app.route('/')
def home():
    return "OK", 200

def run():
    # Render kerkon kete porte
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID)
def handle_admin(message):
    bot.reply_to(message, "👿 Sistemi Sniper u aktivizua!")

if __name__ == "__main__":
    keep_alive()
    print("🤖 Bot is starting...")
    # PERDORIM VETEM KETE: Pa asnje argument shtese qe shkakton error
    bot.infinity_polling()
