
import os
import requests
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# =====================
# CONFIG
# =====================
BOT_TOKEN = os.getenv(8901642018:AAGrilVLPkOlP-pu1ouGVEMlZ6NakD3es2Y)

# Store chat IDs dynamically (no manual CHAT_ID needed)
CHAT_IDS = set()

# =====================
# TELEGRAM COMMANDS
# =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    CHAT_IDS.add(chat_id)

    await update.message.reply_text(
        "🚀 Bot is now active!\n"
        "You will receive low cap alerts here."
    )

# =====================
# SEND MESSAGE TO ALL USERS
# =====================
def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    for chat_id in CHAT_IDS:
        requests.post(url, data={
            "chat_id": chat_id,
            "text": msg
        })

# =====================
# DEX SCANNER
# =====================
def scan():
    url = "https://api.dexscreener.com/latest/dex/search?q=solana"
    data = requests.get(url).json()

    for pair in data.get("pairs", []):
        try:
            name = pair["baseToken"]["name"]
            symbol = pair["baseToken"]["symbol"]

            mc = pair.get("fdv", 0)
            liq = pair.get("liquidity", {}).get("usd", 0)
            vol = pair.get("volume", {}).get("h1", 0)

            buys = pair.get("txns", {}).get("h1", {}).get("buys", 0)
            sells = pair.get("txns", {}).get("h1", {}).get("sells", 0)

            # 🔥 FILTER (low MC + momentum)
            if mc and liq and mc < 500000 and liq > 20000 and buys > sells:

                send(
f"""🚨 LOW CAP GEM ALERT

🪙 {name} ({symbol})
💰 MC: ${mc:,.0f}
💧 Liquidity: ${liq:,.0f}
📈 Volume (1h): ${vol:,.0f}
🟢 Buys: {buys} | 🔴 Sells: {sells}

🔗 {pair['url']}
"""
                )

        except:
            continue

# =====================
# MAIN LOOP
# =====================
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot running...")

    # run bot in background
    import asyncio
    asyncio.create_task(app.run_polling())

    # scanner loop
    while True:
        scan()
        time.sleep(30)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
