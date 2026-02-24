import telebot
import os
from flask import Flask
from threading import Thread

# --- KONFIGURIMI I BLINDUAR ---
TOKEN = "8728522462:AAFCmo5DFol1wzr23sFvZOt--IUx9aukgoU"
ADMIN_ID = 7954635482 

# SHTO kete: threaded=False (shume e rendesishme per Render Free)
bot = telebot.TeleBot(TOKEN, threaded=False) 
app = Flask(__name__)

@app.route('/')
def home():
    return "OK", 200

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID)
def handle_admin(message):
    bot.reply_to(message, "👿 Sistemi Sniper ONLINE 24/7!")

# SHTO kete handler per te testuar nese boti te sheh
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print(f"Mesazh nga: {message.from_user.id}")
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, "Te njoha! Jam gati.")

if __name__ == "__main__":
    keep_alive()
    # Perdorum polling te thjeshte per stabilitet
    bot.polling(none_stop=True, interval=0, timeout=20)
