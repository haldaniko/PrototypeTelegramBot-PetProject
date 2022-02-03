import telebot
from WeatherForecast import *
from ExchangeRates import *
from PrototypeWikipedia import *

bot = telebot.TeleBot("2105876367:AAHtzHrScKaxwzeo654CvvYXOtX9paiiq1Q")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    try:
        msg = message.text.lower() # чтобы на каждый elif не делать лишние трансформации строки, сразу запишем её
        if msg == "привет":
            bot.send_message(message.from_user.id, 'Привет, напиши "Погода"')
        elif msg == "погода":
            bot.send_message(message.from_user.id, '`Погода на сегодня:\n' +
                             request_forecast_today(get_city_id("Kiev")) + "`", parse_mode="Markdown")
        elif msg == "погода завтра":
            bot.send_message(message.from_user.id, '`Погода на завтра:\n' +
                             request_forecast_tomorrow(get_city_id("Kiev")) + "`", parse_mode="Markdown")
        elif msg == "курс":
            bot.send_message(message.from_user.id, '`Курс валют на сегодня:\n' +
                             get_rate_info() + "`", parse_mode="Markdown")
        elif msg.startswith(("что такое ", "расскажи про ", "кто такой ")):
            request = msg.removeprefix('что такое ').removeprefix('расскажи про ').removeprefix('кто такой ')
            bot.send_message(message.from_user.id, 'Ищу информацию про ' + request)
            bot.send_message(message.from_user.id, 'Вот что я нашёл:\n' + prototype_wiki_search(request), parse_mode="Markdown")
        elif msg.startswith(("what is ", "tell me about ", "who is ")):
            request = msg.removeprefix('what is ').removeprefix('tell me about ').removeprefix('who is ')
            bot.send_message(message.from_user.id, 'Looking for ' + request)
            bot.send_message(message.from_user.id, "Look what I've found:\n" + prototype_wiki_search(request, "en"), parse_mode="Markdown")
    except TypeError as e:
        print("Wild Type Error occured! It uses \033[93m", e)
        print('\033[0m')
        pass

bot.polling(none_stop=True, interval=0)
