import telebot
from WeatherForecast import *
from ExchangeRates import *
from RandomFact import *

bot = telebot.TeleBot("2105876367:AAHtzHrScKaxwzeo654CvvYXOtX9paiiq1Q")


@bot.message_handler(content_types=['text'])
def messages(message):
    if message.text.lower() == "привет" or message.text.lower() == "помощь":
        bot.send_message(message.from_user.id, 'Привет! Доступные команды:'
                                               '\n🔸 "Привет"'
                                               '\n🔸 "Погода"'
                                               '\n🔸 "Погода на завтра"'
                                               '\n🔸 "Погода на 5 дней"'
                                               '\n🔸 "Факт дня"'
                                               '\n🔸 "Факт про число"'
                                               '\n🔸 "Шутка"'
                                               '\n🔸 "Цитата"'
                                               '\n🔸 "Курс валют"')
    elif message.text.lower() == "курс валют":
        bot.send_message(message.from_user.id, '`Курс валют на сегодня:\n' +
                         get_rate_info() + "`", parse_mode="Markdown")
    elif message.text.lower() == "погода":
        bot.send_message(message.from_user.id, '`Погода на сегодня:\n' +
                         request_forecast_today(get_city_id("Kiev")) + "`", parse_mode="Markdown")
    elif message.text.lower() == "погода на завтра":
        bot.send_message(message.from_user.id, '`Погода на завтра:\n' +
                         request_forecast_tomorrow(get_city_id("Kiev")) + "`", parse_mode="Markdown")
    elif message.text.lower() == "погода на 5 дней":
        bot.send_message(message.from_user.id, '`Погода на 5 дней:\n' +
                         request_forecast_five(get_city_id("Kiev")) + "`", parse_mode="Markdown")
    elif message.text.lower() == "факт дня":
        bot.send_message(message.from_user.id,
                         '`' + get_today_fact() + "`", parse_mode="Markdown")
    elif message.text.lower() == "факт про число":
        bot.send_message(message.from_user.id,
                         '`' + get_number_fact() + "`", parse_mode="Markdown")
    elif message.text.lower() == "шутка":
        bot.send_message(message.from_user.id,
                         '`' + get_random_joke() + "`", parse_mode="Markdown")
    elif message.text.lower() == "цитата":
        bot.send_message(message.from_user.id,
                         '`' + get_random_quote() + "`", parse_mode="Markdown")
    else:
        bot.send_message(message.from_user.id,
                         'Я пока не знаю что на это ответить. Напиши "помощь"', parse_mode='Markdown')


bot.polling(none_stop=True, interval=0)
