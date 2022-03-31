import telebot
from WeatherForecast import *
from ExchangeRates import *
from RandomFact import *
from PrototypeWikipedia import *

bot = telebot.TeleBot("2105876367:AAHtzHrScKaxwzeo654CvvYXOtX9paiiq1Q")


@bot.message_handler(content_types=['text'])
def messages(message):
    msg = message.text.lower()
    try:
        if msg == "hello" or message.text.lower() == "help":
            bot.send_message(message.from_user.id, 'Hi! Avalaible commands:'
                                                   '\n🔸 "Hello"'
                                                   '\n🔸 "Weather"'
                                                   '\n🔸 "Forecast for tomorrow"'
                                                   '\n🔸 "Forecast for 5 days"'
                                                   '\n🔸 "Fact of the day"'
                                                   '\n🔸 "Fact about number"'
                                                   '\n🔸 "Joke"'
                                                   '\n🔸 "Quote"'
                                                   '\n🔸 "Tell me about ..."'
                                                   '\n🔸 "Exchange Rates"')
        elif msg == "exchange rates":
            bot.send_message(message.from_user.id, '`Exchange rate for today:\n' +
                             get_rate_info() + "`", parse_mode="Markdown")
        elif msg == "weather":
            bot.send_message(message.from_user.id, '`Weather today:\n' +
                             request_forecast_today(get_city_id("Kiev")) + "`", parse_mode="Markdown")
        elif msg == "forecast for tomorrow":
            bot.send_message(message.from_user.id, '`Forecast for tomorrow:\n' +
                             request_forecast_tomorrow(get_city_id("Kiev")) + "`", parse_mode="Markdown")
        elif msg == "forecast for 5 days":
            bot.send_message(message.from_user.id, '`Forecast for 5 days:\n' +
                             request_forecast_five(get_city_id("Kiev")) + "`", parse_mode="Markdown")
        elif msg == "fact of the day":
            bot.send_message(message.from_user.id,
                             '`' + get_today_fact() + "`", parse_mode="Markdown")
        elif msg == "fact about number":
            bot.send_message(message.from_user.id,
                             '`' + get_number_fact() + "`", parse_mode="Markdown")
        elif msg == "joke":
            bot.send_message(message.from_user.id,
                             '`' + get_random_joke() + "`", parse_mode="Markdown")
        elif msg == "quote":
            bot.send_message(message.from_user.id,
                             '`' + get_random_quote() + "`", parse_mode="Markdown")
        elif msg.startswith(("что такое ", "расскажи про ", "кто такой ")):
            request = msg.removeprefix('что такое ').removeprefix('расскажи про ').removeprefix('кто такой ')
            bot.send_message(message.from_user.id, 'Ищу информацию про ' + request)
            bot.send_message(message.from_user.id, 'Вот что я нашёл:\n' + prototype_wiki_search(request),
                             parse_mode="Markdown")
        elif msg.startswith(("what is ", "tell me about ", "who is ")):
            request = msg.removeprefix('what is ').removeprefix('tell me about ').removeprefix('who is ')
            bot.send_message(message.from_user.id, 'Looking for ' + request)
            bot.send_message(message.from_user.id, "Look what I've found:\n" + prototype_wiki_search(request, "en"),
                             parse_mode="Markdown")
        else:
            bot.send_message(message.from_user.id,
                             "I don't know what to answer to that yet. Type 'help'", parse_mode='Markdown')
    except TypeError as e:
        print("Wild Type Error occured! It uses \033[93m", e)
        print('\033[0m')
        pass


bot.polling(none_stop=True, interval=0)
