import telebot
from telebot.types import ReplyKeyboardMarkup
import json
import os
from flask import Flask
import threading

# ================= CONFIG =================
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [6411315434]  # Apna admin ID yaha rakho

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in environment variables")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

DATA_FILE = "usersdata.json"

# ================= DATA FUNCTIONS =================

def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_users(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_user(user):
    users = load_users()
    uid = str(user.id)

    if uid not in users:
        users[uid] = {
            "name": user.first_name,
            "username": user.username
        }
        save_users(users)

        for admin in ADMIN_IDS:
            try:
                bot.send_message(
                    admin,
                    f"🆕 New User Joined\n\n"
                    f"Name: {user.first_name}\n"
                    f"Username: @{user.username}\n"
                    f"ID: {user.id}"
                )
            except:
                pass

# ================= MAIN MENU =================

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📘 Beginner Guide", "📊 Market Concepts")
    markup.add("⚖️ Risk Management", "🧠 Strategy Basics")
    markup.add("❓ FAQ", "📩 Learning Support")
    return markup

# ================= START =================

@bot.message_handler(commands=['start'])
def start(message):
    users = load_users()
    uid = str(message.from_user.id)
    is_new_user = uid not in users

    if is_new_user:
        add_user(message.from_user)

        disclaimer = (
            "⚠️ Disclaimer\n\n"
            "This bot is created for educational purposes only.\n"
            "Trading involves financial risk and may result in loss.\n"
            "We do not provide financial advice, signals, or guaranteed results.\n\n"
            "By continuing, you confirm that you understand and accept this."
        )

        sent = bot.send_message(message.chat.id, disclaimer)

        try:
            bot.pin_chat_message(message.chat.id, sent.message_id)
        except:
            pass

    welcome = (
        f"Welcome {message.from_user.first_name} | to the Market Learning Assistant 📘\n\n"
        "This assistant provides structured educational material\n"
        "for individuals who want to understand financial markets,\n"
        "risk management principles, and disciplined decision-making.\n\n"
        "Inside this bot you will find:\n\n"
        "• Beginner learning modules\n"
        "• Market structure explanations\n"
        "• Risk awareness concepts\n"
        "• Strategy theory (educational)\n"
        "• Frequently asked questions\n\n"
        "All content is shared for informational and educational purposes only.\n"
        "It does not constitute financial advice.\n"
        "Market outcomes vary and no results are guaranteed.\n\n"
        "Please select a section below to begin."
    )

    bot.send_message(message.chat.id, welcome, reply_markup=main_menu())

# ================= MENU CONTENT =================

@bot.message_handler(func=lambda m: m.text == "📘 Beginner Guide")
def beginner(message):
    bot.send_message(message.chat.id,
        "📘 Beginner Guide\n\n"
        "This module introduces foundational concepts\n"
        "for individuals new to financial markets.\n\n"
        "Topics covered:\n\n"
        "• What financial markets are\n"
        "• Basic terminology\n"
        "• How price movements occur (conceptual)\n"
        "• Understanding charts\n"
        "• Responsible participation principles\n\n"
        "Educational reference only.\n"
        "No guarantees implied."
    )

@bot.message_handler(func=lambda m: m.text == "📊 Market Concepts")
def concepts(message):
    bot.send_message(message.chat.id,
        "📊 Market Concepts\n\n"
        "Understanding structure improves clarity.\n\n"
        "This section explains:\n\n"
        "• Trends and ranging conditions\n"
        "• Support and resistance\n"
        "• Volatility basics\n"
        "• Liquidity concepts\n"
        "• Market psychology fundamentals\n\n"
        "These explanations are theoretical\n"
        "and do not represent trading signals\n"
        "or guaranteed outcomes."
    )

@bot.message_handler(func=lambda m: m.text == "⚖️ Risk Management")
def risk(message):
    bot.send_message(message.chat.id,
        "⚖️ Risk Management\n\n"
        "Risk awareness is essential in any financial activity.\n\n"
        "This section covers:\n\n"
        "• Position sizing principles\n"
        "• Exposure control concepts\n"
        "• Risk-reward balance\n"
        "• Emotional discipline\n"
        "• Capital preservation mindset\n\n"
        "Responsible decision-making is emphasized.\n\n"
        "Educational purposes only.\n"
        "Market outcomes vary."
    )

@bot.message_handler(func=lambda m: m.text == "🧠 Strategy Basics")
def strategy(message):
    bot.send_message(message.chat.id,
        "🧠 Strategy Basics\n\n"
        "Strategies are structured frameworks\n"
        "used to analyze market behavior.\n\n"
        "Topics include:\n\n"
        "• Entry and exit theory (conceptual)\n"
        "• Trend-following logic\n"
        "• Reversal concepts\n"
        "• Common beginner mistakes\n"
        "• Importance of back-testing\n\n"
        "No live signals are provided.\n"
        "This is purely educational discussion."
    )

@bot.message_handler(func=lambda m: m.text == "❓ FAQ")
def faq(message):
    bot.send_message(message.chat.id,
        "❓ FAQ\n\n"
        "Q: Do you provide trading signals?\n"
        "A: No. This bot shares educational material only.\n\n"
        "Q: Are profits guaranteed?\n"
        "A: No. Market outcomes vary and no guarantees are implied.\n\n"
        "Q: Is this financial advice?\n"
        "A: No. All content is for informational purposes only.\n\n"
        "Q: Should I invest based on this?\n"
        "A: Always conduct independent research before making financial decisions."
    )

@bot.message_handler(func=lambda m: m.text == "📩 Learning Support")
def support(message):
    bot.send_message(message.chat.id,
        "📩 Learning Support\n\n"
        "If you would like clarification regarding\n"
        "the educational material shared inside this bot,\n"
        "you may reach out for further discussion:\n\n"
        "@Quotexbugtrends1_bot\n\n"
        "Support is limited to educational clarification only.\n"
        "No personal trading advice is provided."
    )

# ================= ADMIN =================

@bot.message_handler(commands=['stats'])
def stats(message):
    if message.from_user.id in ADMIN_IDS:
        users = load_users()
        bot.reply_to(message, f"👥 Total Users: {len(users)}")

@bot.message_handler(commands=['users'])
def users_download(message):
    if message.from_user.id in ADMIN_IDS:
        bot.send_document(message.chat.id, open(DATA_FILE, "rb"))

@bot.message_handler(commands=['broadcast'])
def broadcast_text(message):
    if message.from_user.id in ADMIN_IDS:
        text = message.text.replace("/broadcast ", "")
        users = load_users()
        success = 0
        failed = 0

        for uid in users:
            try:
                bot.send_message(int(uid), text)
                success += 1
            except:
                failed += 1

        bot.reply_to(message,
            f"✅ Broadcast Completed\n\nSuccess: {success}\nFailed: {failed}"
        )

@bot.message_handler(content_types=['photo'])
def broadcast_photo(message):
    if message.from_user.id in ADMIN_IDS:
        users = load_users()
        success = 0
        failed = 0

        for uid in users:
            try:
                bot.send_photo(int(uid), message.photo[-1].file_id, caption=message.caption)
                success += 1
            except:
                failed += 1

        bot.reply_to(message,
            f"✅ Photo Broadcast Completed\n\nSuccess: {success}\nFailed: {failed}"
        )

# ================= WEB ROUTE =================

@app.route('/')
def home():
    return "Bot is running successfully."

# ================= RUN =================

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
