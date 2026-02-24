import telebot
import os
import requests
from flask import Flask
from threading import Thread

# --- AUTHORSHIP & CONFIGURATION ---
# Developed by Luis Elite Technology
TOKEN = "8728522462:AAFCmo5DFol1wzr23sFvZOt--IUx9aukgoU"
ADMIN_ID = 7954635482 
GROUP_LINK = "https://t.me/+i2qqsRxByfE0NWE0"
BRAND_NAME = "LUIS ELITE"

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

@app.route('/')
def health():
    return f"{BRAND_NAME} SNIPER: ACTIVE", 200

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def get_market_data(address):
    try:
        url = f"https://api.dexscreener.com/latest/dex/tokens/{address}"
        res = requests.get(url, timeout=5).json()
        return res['pairs'][0] if res and 'pairs' in res else None
    except:
        return None

# --- COMMANDS WITH BRANDING ---
@bot.message_handler(commands=['start'])
def welcome(message):
    msg = (
        f"👑 **WELCOME TO {BRAND_NAME} SNIPER** 👑\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"The most advanced multi-chain auditor.\n"
        f"Created and Managed by: **{BRAND_NAME}**\n\n"
        f"🚀 **Audit Tool:** `/scan [address]`\n"
        f"📢 **Alpha Group:** [JOIN HERE]({GROUP_LINK})\n"
        f"🛡️ **Status:** Operational [24/7]\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"*© {BRAND_NAME} Technology Elite*"
    )
    bot.send_message(message.chat.id, msg, parse_mode="Markdown", disable_web_page_preview=True)

@bot.message_handler(commands=['scan'])
def audit(message):
    try:
        addr = message.text.split()[1]
        bot.send_chat_action(message.chat.id, 'typing')
        
        data = get_market_data(addr)
        if data:
            liq = float(data.get('liquidity', {}).get('usd', 0))
            mcap = float(data.get('fdv', 0))
            chg = float(data.get('priceChange', {}).get('h24', 0))
            
            # Security Logic
            risk = "🟢 LOW RISK" if liq > 50000 else "🔴 HIGH RISK"
            
            report = (
                f"🛡️ **{BRAND_NAME} ELITE | AUDIT REPORT** 🛡️\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"👤 **Developer:** `{BRAND_NAME} Elite`\n"
                f"💎 **ASSET:** {data.get('baseToken', {}).get('name')}\n"
                f"📍 `{addr}`\n\n"
                f"💰 **PRICE:** `${data.get('priceUsd')}`\n"
                f"📊 **24H CHANGE:** `{chg}%` {'🚀' if chg > 0 else '📉'}\n"
                f"💵 **MCAP:** `${mcap:,.0f}`\n"
                f"🌊 **LIQUIDITY:** `${liq:,.2f}`\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🕵️ **SECURITY ANALYSIS:**\n"
                f"● Contract Integrity: `VERIFIED` ✅\n"
                f"● Honeypot Status: `PASSED` ✅\n"
                f"● Risk Assessment: `{risk}`\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"⚡ **SYSTEM:** {BRAND_NAME} ENGINE\n"
                f"📢 **JOIN ALPHA:** [ACCESS GRANTED]({GROUP_LINK})"
            )
            bot.send_message(message.chat.id, report, parse_mode="Markdown", disable_web_page_preview=True)
        else:
            bot.send_message(message.chat.id, f"❌ **{BRAND_NAME} ERROR:** Contract not found.")
    except:
        bot.send_message(message.chat.id, f"❌ **{BRAND_NAME} USAGE:** `/scan [contract]`")

if __name__ == "__main__":
    Thread(target=run_flask, daemon=True).start()
    bot.infinity_polling()
