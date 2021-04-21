import telebot as tel_api

from help_center.tel_bot_api import bot_api

bot = tel_api.TeleBot('1730788276:AAFDK_DxwP4s5ULAc3SiyAYpzIfwewx4t-c')

bot_api.init_bot_sender(bot.send_message)


@bot.message_handler(commands=['admin'])
def admin_command(message):
    bot_api.set_admin(message.from_user.id)
    bot.send_message(message.chat.id, "Save you as admin")

@bot.message_handler(commands=['manager'])
def admin_command(message):
    bot_api.set_manager(message.from_user.id)
    bot.send_message(message.chat.id, "Save you as manager")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    print(message.text)
    try:
        bot_api.handle_message(message)
    except:
        print('Ops, we failed')


bot.polling(none_stop=True, interval=0)
