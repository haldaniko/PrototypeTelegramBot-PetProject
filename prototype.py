import telebot
from WeatherForecast import *
from ExchangeRates import *

bot = telebot.TeleBot("2105876367:AAHtzHrScKaxwzeo654CvvYXOtX9paiiq1Q")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == "привет":
        bot.send_message(message.from_user.id, 'Привет, напиши "Погода"')
    elif message.text.lower() == "погода":
        bot.send_message(message.from_user.id, '`Погода на сегодня:\n' +
                         request_forecast_today(get_city_id("Kiev")) + "`", parse_mode="Markdown")
    elif message.text.lower() == "курс":
        bot.send_message(message.from_user.id, '`Курс валют на сегодня:\n' +
                         get_rate_info() + "`", parse_mode="Markdown")


bot.polling(none_stop=True, interval=0)
