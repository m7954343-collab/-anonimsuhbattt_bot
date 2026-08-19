import telebot
from telebot import types

TOKEN = "8854185072:AAFApDH0X07i6QD5agT73uitMAmBXsIRfMQ"
bot = telebot.TeleBot(TOKEN)

# Foydalanuvchilar va ulangan chatlar ro'yxati
users = {}
waiting_users = []
active_chats = {}

def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔎 Suhbatdosh qidirish", "❌ Suhbatni yakunlash")
    return markup

def gender_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("👨 O'g'il bola", "👩 Qiz bola")
    return markup

@bot.message_handler(commands=['start'])
def start_command(message):
    chat_id = message.chat.id
    users[chat_id] = {'gender': None, 'search_gender': None}
    bot.send_message(chat_id, "Xush kelibsiz! Avval o'z jinsingizni tanlang:", reply_markup=gender_keyboard())

@bot.message_handler(func=lambda msg: msg.text in ["👨 O'g'il bola", "👩 Qiz bola"])
def set_gender(message):
    chat_id = message.chat.id
    if chat_id not in users:
        users[chat_id] = {}
    users[chat_id]['gender'] = message.text
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("👨 O'g'il bola izlash", "👩 Qiz bola izlash")
    bot.send_message(chat_id, "Kim bilan suhbatlashmoqchisiz?", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text in ["👨 O'g'il bola izlash", "👩 Qiz bola izlash"])
def set_search_gender(message):
    chat_id = message.chat.id
    if chat_id not in users:
        users[chat_id] = {}
    users[chat_id]['search_gender'] = message.text
    
    bot.send_message(
        chat_id, 
        "Sozlamalar saqlandi! Pastdagi tugma orqali qidiruvni boshlang.", 
        reply_markup=main_keyboard()
    )

@bot.message_handler(func=lambda msg: msg.text == "🔎 Suhbatdosh qidirish")
def search_partner(message):
    chat_id = message.chat.id
    
    if chat_id in active_chats:
        bot.send_message(chat_id, "Siz allaqachon suhbatdasiz!")
        return

    if chat_id in waiting_users:
        bot.send_message(chat_id, "Suhbatdosh qidirilmoqda... Kuting.")
        return

    if waiting_users:
        partner_id = waiting_users.pop(0)
        active_chats[chat_id] = partner_id
        active_chats[partner_id] = chat_id
        
        bot.send_message(chat_id, "🎉 Suhbatdosh topildi! Yozishishingiz mumkin.", reply_markup=main_keyboard())
        bot.send_message(partner_id, "🎉 Suhbatdosh topildi! Yozishishingiz mumkin.", reply_markup=main_keyboard())
    else:
        waiting_users.append(chat_id)
        bot.send_message(chat_id, "🔎 Suhbatdosh qidirilmoqda... Kuting.")

@bot.message_handler(func=lambda msg: msg.text == "❌ Suhbatni yakunlash")
def stop_chat(message):
    chat_id = message.chat.id
    
    if chat_id in active_chats:
        partner_id = active_chats.pop(chat_id)
        if partner_id in active_chats:
            del active_chats[partner_id]
            
        bot.send_message(chat_id, "🛑 Suhbat yakunlandi.", reply_markup=main_keyboard())
        bot.send_message(partner_id, "🛑 Suhbatdosh suhbatni yakunladi.", reply_markup=main_keyboard())
    elif chat_id in waiting_users:
        waiting_users.remove(chat_id)
        bot.send_message(chat_id, "🛑 Qidiruv bekor qilindi.", reply_markup=main_keyboard())
    else:
        bot.send_message(chat_id, "Siz hozircha hech kim bilan suhbatlashmayapsiz.")

@bot.message_handler(func=lambda message: True)
def relay_message(message):
    chat_id = message.chat.id
    if chat_id in active_chats:
        partner_id = active_chats[chat_id]
        bot.send_message(partner_id, message.text)
    else:
        bot.send_message(chat_id, "Suhbatlashish uchun '🔎 Suhbatdosh qidirish' tugmasini bosing.")

print("Bot muvaffaqiyatli ishga tushdi...")
bot.infinity_polling(skip_pending=True)
      
