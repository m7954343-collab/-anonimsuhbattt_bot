import telebot

# Bot tokeningizni qo'ying
TOKEN = 'BOT_TOKENINGIZNI_SHU_YERGA_YOZING'
bot = telebot.TeleBot(TOKEN)

# Juftliklarni saqlash uchun lug'at
user_pairs = {}
waiting_users = []

@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id, 
        "Suhbatdosh qidirish uchun /search buyrug'ini bosing.\n"
        "Suhbatni to'xtatish uchun /stop buyrug'ini bosing."
    )

@bot.message_handler(commands=['search'])
def search_partner(message):
    chat_id = message.chat.id
    
    if chat_id in user_pairs:
        bot.send_message(chat_id, "Siz allaqachon suhbatdasiz!")
        return
        
    if chat_id in waiting_users:
        bot.send_message(chat_id, "Suhbatdosh qidirilmoqda, kuting...")
        return

    if waiting_users:
        partner_id = waiting_users.pop(0)
        user_pairs[chat_id] = partner_id
        user_pairs[partner_id] = chat_id
        
        bot.send_message(chat_id, "Suhbatdosh topildi! Yozishishingiz mumkin.")
        bot.send_message(partner_id, "Suhbatdosh topildi! Yozishishingiz mumkin.")
    else:
        waiting_users.append(chat_id)
        bot.send_message(chat_id, "Suhbatdosh qidirilmoqda...")

@bot.message_handler(commands=['stop'])
def stop_chat(message):
    chat_id = message.chat.id
    
    if chat_id in user_pairs:
        partner_id = user_pairs.pop(chat_id)
        if partner_id in user_pairs:
            del user_pairs[partner_id]
            
        bot.send_message(chat_id, "Suhbat yakunlandi.")
        bot.send_message(partner_id, "Suhbatdosh suhbatni yakunladi.")
    elif chat_id in waiting_users:
        waiting_users.remove(chat_id)
        bot.send_message(chat_id, "Qidiruv to'xtatildi.")
    else:
        bot.send_message(chat_id, "Siz hozircha hech kim bilan suhbatlashmayapsiz.")

@bot.message_handler(func=lambda message: True)
def relay_message(message):
    chat_id = message.chat.id
    
    if chat_id in user_pairs:
        partner_id = user_pairs[chat_id]
        try:
            bot.send_message(partner_id, message.text)
        except Exception:
            bot.send_message(chat_id, "Xabar yuborishda xatolik yuz berdi.")
    else:
        bot.send_message(chat_id, "Suhbatdosh topish uchun /search buyrug'ini bosing.")

# Botni uzluksiz fonda ishlatib turuvchi asosiy qism
if __name__ == '__main__':
    bot.infinity_polling(skip_pending=True)
    
