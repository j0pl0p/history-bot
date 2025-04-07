import telebot

from secret_file import secret_token

bot = telebot.TeleBot(secret_token())


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, message.text)


bot.polling(none_stop=True, interval=0)
