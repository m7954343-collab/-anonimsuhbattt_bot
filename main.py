import os
import telebot

# Tokenni Render'dan avtomatik oladi
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

user_pairs = {}
waiting_users = []

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Suhbatdosh qidirish uchun /search bosing.")

@bot.message_handler(commands=['search'])
def search_partner(message):
    chat_id = message.chat.id
    if chat_id in user_pairs or chat_id in waiting_users:
        bot.send_message(chat_id, "Kutib turing...")
        return

    if waiting_users:
        partner_id = waiting_users.pop(0)
        user_pairs[chat_id] = partner_id
        user_pairs[partner_id] = chat_id
        bot.send_message(chat_id, "Suhbatdosh topildi!")
        bot.send_message(partner_id, "Suhbatdosh topildi!")
    else:
        waiting_users.append(chat_id)
        bot.send_message(chat_id, "Suhbatdosh qidirilmoqda...")

@bot.message_handler(func=lambda message: True)
def relay_message(message):
    chat_id = message.chat.id
    if chat_id in user_pairs:
        bot.send_message(user_pairs[chat_id], message.text)

if __name__ == '__main__':
    bot.infinity_polling(skip_pending=True)
        
