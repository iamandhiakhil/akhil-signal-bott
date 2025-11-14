from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_signal(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, data=data)

@app.route("/", methods=["GET"])
def home():
    return "Akhil Signal Bot Running"

@app.route("/webhook", methods=["POST"])
def webhook():
    alert = request.json

    symbol = alert.get("symbol", "Unknown")
    price = alert.get("price", "Unknown")
    time = alert.get("time", "Unknown")
    signal = alert.get("signal", "Unknown")
    tf = alert.get("tf", "Unknown")

    msg = f"🚨 <b>NEW SIGNAL</b>\n\n" \
          f"📌 <b>Symbol:</b> {symbol}\n" \
          f"⏱ <b>Timeframe:</b> {tf}\n" \
          f"💰 <b>Price:</b> {price}\n" \
          f"📅 <b>Time:</b> {time}\n" \
          f"📍 <b>Signal:</b> {signal}\n"

    send_signal(msg)

    return {"status": "success"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
