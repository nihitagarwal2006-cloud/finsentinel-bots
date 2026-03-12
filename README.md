# FinSentinel — Telegram + WhatsApp Bot 🤖🛡️

One server, two bots. Built for India 🇮🇳

---

## Setup Guide

### Step 1 — Get Your Keys

#### Telegram Bot Token (5 minutes)
1. Open Telegram → search **@BotFather**
2. Send `/newbot`
3. Name: `FinSentinel`
4. Username: `FinSentinelBot` (or any available name)
5. BotFather gives you a token like:
   `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
6. Copy it ✅

#### Twilio WhatsApp (10 minutes)
1. Go to **twilio.com** → Sign up free
2. Verify your phone number
3. Go to **Console Dashboard** → copy:
   - `Account SID`
   - `Auth Token`
4. Go to **Messaging → Try it out → Send a WhatsApp message**
5. Note the sandbox number (e.g. `+14155238886`)
6. **Join the sandbox** — send `join <word>` to that number on WhatsApp ✅

#### Anthropic API Key
1. Go to **console.anthropic.com**
2. API Keys → Create Key
3. Copy it ✅

---

### Step 2 — Deploy on Render

1. Push this folder to a **new GitHub repo**
   - Name: `finsentinel-bots`
2. Go to **render.com** → New → Web Service
3. Connect the repo
4. Settings:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`
5. Add **Environment Variables**:

| Key | Value |
|-----|-------|
| `ANTHROPIC_API_KEY` | your Anthropic key |
| `TELEGRAM_TOKEN` | your Telegram bot token |
| `TWILIO_SID` | your Twilio Account SID |
| `TWILIO_AUTH` | your Twilio Auth Token |
| `TWILIO_NUMBER` | `whatsapp:+14155238886` |

6. Click **Deploy** → wait 2-3 min → get your URL ✅

---

### Step 3 — Connect Telegram

1. Visit this URL in your browser:
   ```
   https://YOUR-RENDER-URL.onrender.com/setup?url=https://YOUR-RENDER-URL.onrender.com
   ```
2. You'll see: `✅ Telegram webhook set`
3. Open Telegram → find your bot → send `/start` ✅

---

### Step 4 — Connect WhatsApp (Twilio)

1. Go to Twilio → **Messaging → Settings → WhatsApp Sandbox Settings**
2. Set **"When a message comes in"** webhook:
   ```
   https://YOUR-RENDER-URL.onrender.com/whatsapp
   ```
3. Method: **HTTP POST**
4. Save ✅
5. Send any message to the Twilio sandbox number on WhatsApp ✅

---

## Test It!

**Telegram:** Find your bot → send:
```
Congratulations! You won ₹50,000. Send Aadhaar to claim prize.
```

**WhatsApp:** Send to Twilio number:
```
URGENT: Your SBI KYC expires today. Click http://sbi-fake.xyz
```

Both should reply with full scam analysis! 🎉

---

## What Both Bots Can Do

| Feature | Works |
|---------|-------|
| Analyze scam text messages | ✅ |
| Check suspicious URLs | ✅ |
| Check UPI IDs for fraud | ✅ |
| Analyze screenshot images | ✅ |
| Show emergency helplines | ✅ |
| Multi-language support | ✅ |

---

## Webhook URLs

| Bot | Webhook URL |
|-----|------------|
| Telegram | `https://your-url.onrender.com/telegram` |
| WhatsApp | `https://your-url.onrender.com/whatsapp` |
| Health check | `https://your-url.onrender.com/` |

---

## Built By
**Nihit & Anchal** 🇮🇳
🌐 https://kaleidoscopic-pony-52e4b9.netlify.app
📞 Cybercrime Helpline: 1930
