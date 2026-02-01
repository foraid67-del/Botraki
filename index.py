from flask import Flask, request
import telebot
import os

app = Flask(__name__)

# Ваш токен бота
TOKEN = os.environ.get('BOT_TOKEN', 'ВАШ_ТОКЕН')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    text = """
🤖 SWILL Intelligence Bot

📱 Поиск по номеру:
• Просто отправьте номер телефона
• Или /search номер

📲 Поиск Telegram:
• Отправьте @username

👤 Поиск ВКонтакте:
• Отправьте vk.com/id1

✅ Бот работает на Vercel!
"""
    bot.reply_to(message, text)

@bot.message_handler(commands=['search'])
def search_cmd(message):
    try:
        phone = message.text.split()[1]
        result = f"""
📱 Поиск: {phone}
🔗 VK: https://vk.com/phone/{phone}
📞 WhatsApp: https://wa.me/{phone}
"""
        bot.reply_to(message, result)
    except:
        bot.reply_to(message, "Используйте: /search 79001234567")

@bot.message_handler(func=lambda m: True)
def all_messages(message):
    text = message.text
    
    # Если номер телефона
    if any(c.isdigit() for c in text) and len(text) >= 10:
        phone = ''.join(filter(str.isdigit, text))
        reply = f"🔍 Найден номер: {phone}\n📱 VK: vk.com/phone/{phone}"
        bot.reply_to(message, reply)
    
    # Если Telegram username
    elif '@' in text:
        username = text.replace('@', '')
        reply = f"📲 Telegram: @{username}\n🔗 t.me/{username}"
        bot.reply_to(message, reply)
    
    else:
        bot.reply_to(message, "Отправьте номер телефона или @username")

@app.route('/')
def home():
    return "🤖 Bot is running"

@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'OK', 200

if __name__ == '__main__':
    app.run()