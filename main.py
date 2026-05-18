import requests
import time

BOT_TOKEN = "8901642018:AAGrilVLPkOlP-pu1ouGVEMlZ6NakD3es2Y"
CHAT_ID = "8883006540"

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })

def scan():
    url = "https://api.dexscreener.com/latest/dex/search?q=solana"
    data = requests.get(url).json()

    for pair in data.get("pairs", []):
        try:
            mc = pair.get("fdv", 0)
            liq = pair.get("liquidity", {}).get("usd", 0)

            if mc and liq and mc < 200000 and liq > 15000:

                send(f'''
🚨 NEW COIN ALERT

Name: {pair['baseToken']['name']}
MC: ${mc}
Liquidity: ${liq}

{pair['url']}
''')

        except:
            pass

while True:
    scan()
    time.sleep(30)
