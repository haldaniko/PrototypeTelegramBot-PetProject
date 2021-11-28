import telebot
from request import *


bot = telebot.TeleBot("2105876367:AAHtzHrScKaxwzeo654CvvYXOtX9paiiq1Q")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, 'Привет, напиши "Погода"')
    elif message.text == "Погода":
        city_id = get_city_id("Kiev")
        mes = request_forecast(city_id)
        bot.send_message(message.from_user.id, str(mes))


bot.polling(none_stop=True, interval=0)
