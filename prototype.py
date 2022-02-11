import telebot
from WeatherForecast import *
from ExchangeRates import *
from RandomFact import *
from PrototypeWikipedia import *

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
