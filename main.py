import telebot
import os
import requests
from flask import Flask
from threading import Thread

# --- KONFIGURIMI I BLINDUAR ---
TOKEN = "8728522462:AAFCmo5DFol1wzr23sFvZOt--IUx9aukgoU"
ADMIN_ID = 7954635482 

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

# --- FUNKSIONI REAL I SKANIMIT (DEXSCREENER API) ---
def get_token_data(address):
    try:
        url = f"https://api.dexscreener.com/latest/dex/tokens/{address}"
        response = requests.get(url, timeout=10)
        data = response.json()
        if data and 'pairs' in data:
            return data['pairs'][0]
        return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID, commands=['start'])
def handle_admin(message):
    bot.reply_to(message, "👿 Sistemi Sniper ONLINE!\nPërdor `/scan adresa` për të parë tregun në kohë reale.")

@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID, commands=['scan'])
def scan_contract(message):
    try:
        contract_address = message.text.split()[1]
        bot.send_chat_action(message.chat.id, 'typing')
        
        token_data = get_token_data(contract_address)
        
        if token_data:
            name = token_data.get('baseToken', {}).get('name', 'N/A')
            symbol = token_data.get('baseToken', {}).get('symbol', 'N/A')
            price = token_data.get('priceUsd', '0')
            mcap = token_data.get('fdv', 'N/A')
            liquidity = token_data.get('liquidity', {}).get('usd', 'N/A')
            change = token_data.get('priceChange', {}).get('h24', '0')

            report = (
                f"📊 **RAPORTI I TREGUT: {name} ({symbol})** 📊\n\n"
                f"💰 Çmimi: `${price}`\n"
                f"📈 Ndryshimi 24h: `{change}%`\n"
                f"💎 MCap: `${mcap}`\n"
                f"🌊 Liquidity: `${liquidity}`\n\n"
                f"📍 Kontrata: `{contract_address}`\n\n"
                f"🔥 **Statusi: LIVE DATA**"
            )
        else:
            report = f"⚠️ Nuk u gjetën të dhëna në DEX për:\n`{contract_address}`\n\nSigurohu që ka likuiditet të shtuar."

        bot.send_message(message.chat.id, report, parse_mode="Markdown")
        
    except IndexError:
        bot.reply_to(message, "❌ Përdor: `/scan adresa_e_kontrates`")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
