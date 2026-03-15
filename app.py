from flask import Flask, request, jsonify
import anthropic
import requests
import os
import json

app = Flask(__name__)

# ── CONFIG (set as environment variables on Render) ──
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
TELEGRAM_TOKEN   = os.environ.get("TELEGRAM_TOKEN", "")
TWILIO_SID       = os.environ.get("TWILIO_SID", "")
TWILIO_AUTH      = os.environ.get("TWILIO_AUTH", "")
TWILIO_NUMBER    = os.environ.get("TWILIO_NUMBER", "whatsapp:+14155238886")  # Twilio sandbox number

# Validate API key on startup
if not ANTHROPIC_API_KEY:
    print("❌ CRITICAL: ANTHROPIC_API_KEY is not set! All analysis will fail.")
else:
    print(f"✅ Anthropic API key loaded ({ANTHROPIC_API_KEY[:12]}...)")

if not TELEGRAM_TOKEN:
    print("⚠️ WARNING: TELEGRAM_TOKEN is not set!")
else:
    print(f"✅ Telegram token loaded ({TELEGRAM_TOKEN[:10]}...)")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None

def get_client():
    if not client:
        raise Exception("ANTHROPIC_API_KEY not configured. Please set it in Render environment variables.")
    return client

# ════════════════════════════════════════════════
#  SHARED AI FUNCTIONS
# ════════════════════════════════════════════════

def analyze_scam(message):
    try:
        response = get_client().messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=400,
            messages=[{"role": "user", "content": f"""You are FinSentinel, an AI financial scam detector for India.
Analyze this message for scam patterns.

Message: \"\"\"{message}\"\"\"

Reply in this exact format (WhatsApp/Telegram friendly):

[emoji] *VERDICT: SCAM / SUSPICIOUS / SAFE*
📊 *Risk Score: X/100*

⚠️ *Red Flags:*
• flag 1
• flag 2

✅ *What To Do:*
• action 1
• action 2

📞 *Helpline: 1930*

Rules:
- 🚨 for SCAM (70-100), ⚠️ for SUSPICIOUS (30-69), ✅ for SAFE (0-29)
- Max 120 words
- Simple language for non-tech Indian users"""}]
        )
        return response.content[0].text
    except Exception as e:
        return "⚠️ Analysis failed. Please try again.\n\n📞 If urgent, call *1930*"


def check_upi(upi_id):
    try:
        response = get_client().messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=250,
            messages=[{"role": "user", "content": f"""You are a UPI fraud expert in India. Analyze this UPI ID like a real expert warning a friend.

UPI ID: {upi_id}

Check for: prize/winner/reward/lucky/refund/kyc/urgent/govt impersonation/wrong bank handle/random numbers/fake names.

Reply format:
💳 *UPI Check: {upi_id}*
[emoji] *[FRAUDULENT / SUSPICIOUS / LOOKS SAFE]*
📊 _Risk: X/100_

[One sentence like a real person — e.g. "Yaar, 'prize' wala UPI ID kabhi genuine nahi hota."]

⚠️ *Red flag:* [specific reason about THIS UPI ID]
✅ *Advice:* [specific advice]

📞 _Report fraud: 1930_

Use 🚨 FRAUDULENT, ⚠️ SUSPICIOUS, ✅ LOOKS SAFE. Max 80 words. Sound human and warm."""}]
        )
        return response.content[0].text
    except Exception as e:
        print(f"UPI check error: {e}")
        return "⚠️ UPI check failed. Please try again in a moment."


def check_url(url):
    try:
        response = get_client().messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=200,
            messages=[{"role": "user", "content": f"""Check if this URL is a phishing/scam link for India: {url}
Look for: misspelled domains, fake bank names, suspicious TLDs, URL shorteners, urgency keywords.

Reply format:
🔗 *URL CHECK*
[emoji] *Result: DANGEROUS / SUSPICIOUS / LOOKS SAFE*
📊 *Risk: X/100*
⚠️ *Red flags:* brief
✅ *Action:* what to do
📞 *Report: 1930*

Use 🚨 DANGEROUS, ⚠️ SUSPICIOUS, ✅ LOOKS SAFE. Max 60 words."""}]
        )
        return response.content[0].text
    except:
        return "⚠️ Couldn't check URL. *Never click suspicious links.* Call 1930 if needed."


def route_message(text):
    """Route message to correct handler based on content"""
    t = text.strip()
    tl = t.lower()

    # Greetings
    if tl in ["hi","hello","hey","start","help","hii","namaste","/start","/help"]:
        return get_welcome()

    # About
    if tl in ["about","who are you","what are you","/about"]:
        return ("🛡️ *FinSentinel — AI Financial Scam Detector* 🇮🇳\n\n"
                "I use AI to detect financial scams instantly.\n\n"
                "🌐 finsentinel.netlify.app\n"
                "👨‍💻 Built by Nihit & Anchal\n\n"
                "Send me any suspicious message to analyze!")

    # Emergency
    if any(w in tl for w in ["1930","helpline","emergency","report fraud","/helpline"]):
        return ("🚨 *Emergency Contacts*\n\n"
                "📞 *Cybercrime Helpline:* 1930\n"
                "🌐 *File complaint:* cybercrime.gov.in\n\n"
                "📞 *Bank Fraud Lines:*\n"
                "• SBI: 1800-11-2211\n"
                "• HDFC: 1800-202-6161\n"
                "• ICICI: 1800-200-3344\n"
                "• Axis: 1800-419-5959\n"
                "• Paytm: 0120-3888388\n"
                "• PhonePe: 080-68727374\n"
                "• GPay: 1800-419-0157\n\n"
                "⚡ *Act within the first hour if scammed!*")

    # UPI ID
    if "@" in t and len(t) < 60 and " " not in t:
        return check_upi(t)

    # URL
    if tl.startswith("http") or "www." in tl:
        return check_url(t)

    # Too short
    if len(t) < 15:
        return ("🤔 Message too short to analyze.\n\n"
                "Please send the *full suspicious message* you received.\n\n"
                "Type *help* to see all commands.")

    # Full analysis
    return analyze_scam(t)


def get_welcome():
    return ("🛡️ *Welcome to FinSentinel!*\n"
            "_AI-Powered Scam Detector for India_ 🇮🇳\n\n"
            "I can detect:\n"
            "💬 *Scam messages* — paste any suspicious SMS/text\n"
            "🔗 *Phishing links* — send any suspicious URL\n"
            "💳 *UPI fraud* — send a UPI ID (e.g. prize@paytm)\n"
            "📞 *Emergency* — type *helpline* for contacts\n\n"
            "━━━━━━━━━━━━━━━\n"
            "📌 Just send me the suspicious message — that's it!\n\n"
            "🚨 *Emergency:* Call *1930*\n"
            "🌐 finsentinel.netlify.app\n\n"
            "_Built by Nihit & Anchal • Free forever_ ❤️")


# ════════════════════════════════════════════════
#  TELEGRAM BOT
# ════════════════════════════════════════════════

def send_telegram(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    })


@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    data = request.json
    try:
        msg = data.get("message") or data.get("edited_message")
        if not msg:
            return "OK", 200

        chat_id = msg["chat"]["id"]
        msg_type = "text" if "text" in msg else "photo" if "photo" in msg else "other"

        if msg_type == "text":
            text = msg["text"]
            print(f"📱 Telegram from {chat_id}: {text}")
            reply = route_message(text)
            send_telegram(chat_id, reply)

        elif msg_type == "photo":
            # Get highest quality photo
            photo = msg["photo"][-1]
            file_id = photo["file_id"]
            caption = msg.get("caption", "")

            # Get file path
            file_info = requests.get(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getFile?file_id={file_id}"
            ).json()
            file_path = file_info["result"]["file_path"]
            file_url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_path}"

            # Download image
            img_data = requests.get(file_url).content
            import base64
            img_b64 = base64.b64encode(img_data).decode("utf-8")

            send_telegram(chat_id, "🖼️ Analyzing your screenshot...")
            reply = analyze_image(img_b64, caption)
            send_telegram(chat_id, reply)

        else:
            send_telegram(chat_id,
                "👋 I can analyze text messages, URLs, UPI IDs and screenshots.\n\n"
                "Just send me a suspicious message or image!")

    except Exception as e:
        print(f"Telegram error: {e}")

    return "OK", 200


def setup_telegram_webhook(base_url):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"
    response = requests.post(url, json={"url": f"{base_url}/telegram"})
    print(f"Telegram webhook: {response.json()}")


# ════════════════════════════════════════════════
#  WHATSAPP BOT (TWILIO)
# ════════════════════════════════════════════════

def send_whatsapp(to, text):
    from twilio.rest import Client
    twilio_client = Client(TWILIO_SID, TWILIO_AUTH)
    twilio_client.messages.create(
        body=text,
        from_=TWILIO_NUMBER,
        to=to
    )


@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    try:
        incoming = request.form.get("Body", "").strip()
        sender   = request.form.get("From", "")
        num_media = int(request.form.get("NumMedia", 0))

        print(f"📱 WhatsApp from {sender}: {incoming}")

        if num_media > 0:
            # Image received
            media_url = request.form.get("MediaUrl0", "")
            media_type = request.form.get("MediaContentType0", "image/jpeg")

            img_data = requests.get(
                media_url,
                auth=(TWILIO_SID, TWILIO_AUTH)
            ).content
            import base64
            img_b64 = base64.b64encode(img_data).decode("utf-8")

            send_whatsapp(sender, "🖼️ Analyzing your screenshot...")
            reply = analyze_image(img_b64, incoming)
        else:
            reply = route_message(incoming)

        send_whatsapp(sender, reply)

    except Exception as e:
        print(f"WhatsApp error: {e}")

    return "OK", 200


# ════════════════════════════════════════════════
#  IMAGE ANALYSIS (shared)
# ════════════════════════════════════════════════

def analyze_image(img_b64, caption=""):
    try:
        prompt = (f"You are FinSentinel, AI scam detector for India. "
                  f"Analyze this screenshot for financial scams.\n"
                  f"{'Caption: ' + caption if caption else ''}\n\n"
                  f"Reply format:\n"
                  f"🖼️ *SCREENSHOT ANALYSIS*\n"
                  f"[emoji] *Verdict: SCAM / SUSPICIOUS / SAFE*\n"
                  f"📊 *Risk: X/100*\n"
                  f"⚠️ *Found:* what you see\n"
                  f"🚩 *Red flags:* list\n"
                  f"✅ *Action:* what to do\n"
                  f"📞 *Helpline: 1930*\n\n"
                  f"Use 🚨 SCAM, ⚠️ SUSPICIOUS, ✅ SAFE. Max 100 words.")

        response = get_client().messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=350,
            messages=[{"role": "user", "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": img_b64}},
                {"type": "text",  "text": prompt}
            ]}]
        )
        return response.content[0].text
    except Exception as e:
        return ("🖼️ Couldn't analyze the image.\n\n"
                "Please type out the suspicious message as text.\n\n"
                "📞 If urgent, call *1930*")


# ════════════════════════════════════════════════
#  HEALTH CHECK & SETUP
# ════════════════════════════════════════════════

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "✅ FinSentinel Bots running",
        "telegram": "active" if TELEGRAM_TOKEN else "not configured",
        "whatsapp": "active" if TWILIO_SID else "not configured",
        "built_by": "Nihit & Anchal 🇮🇳"
    })


@app.route("/setup", methods=["GET"])
def setup():
    base_url = request.args.get("url", "")
    if base_url and TELEGRAM_TOKEN:
        setup_telegram_webhook(base_url)
        return f"✅ Telegram webhook set to {base_url}/telegram"
    return "Pass ?url=https://your-render-url.onrender.com to set up Telegram webhook"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 FinSentinel Bots starting on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
