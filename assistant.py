import telebot
import schedule
import time
from WeatherForecast import *
from BankAccounting import *
from GetRequests import *
from SearchWikipedia import *
from googletrans import Translator
from multiprocessing import Process


bot = telebot.TeleBot(config.botToken)
translator = Translator()


def morning_news():
    bot.send_message(5157350956, "С добрым утром!")


def menu(message):
    try:
        if message.text == "💰 Фінанси":

            keyboard = telebot.types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
            exchangeButton = telebot.types.KeyboardButton(text="💱 Курс валют")
            returnButton = telebot.types.KeyboardButton(text="🔸 Назад")
            keyboard.add(exchangeButton, returnButton)

            bot.send_message(message.chat.id,
                             text="💸 Фінансовий куточок\n\n{}".format(mono_get_client_info()),
                             parse_mode="Markdown",
                             reply_markup=keyboard)

            bot.register_next_step_handler(message, finance_menu)

        elif message.text == "⚒ Інструменти":

            keyboard = telebot.types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
            weatherButton = telebot.types.KeyboardButton(text="🌦 Погода")
            wikipediaButton = telebot.types.KeyboardButton(text="📖 Пошук у Вікі")
            translateButton = telebot.types.KeyboardButton(text="📝 Перекладач")
            returnButton = telebot.types.KeyboardButton(text="🔸 Назад")
            keyboard.add(weatherButton, wikipediaButton, translateButton, returnButton)
            bot.send_message(message.chat.id, text="🔸 Панель інструментів",
                             parse_mode="Markdown",
                             reply_markup=keyboard)

            bot.register_next_step_handler(message, tools_menu)

        elif message.text == "🎨 Розваги":

            keyboard = telebot.types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
            returnButton = telebot.types.KeyboardButton(text="🔸 Назад")
            keyboard.add(returnButton)

            bot.send_message(message.chat.id, text="Тут поки нічо нема",
                             parse_mode="Markdown",
                             reply_markup=keyboard)

            bot.register_next_step_handler(message, start)
    except TypeError as e:
        print("Wild Type Error occured! It uses \033[93m", e)
        print('\033[0m')
        pass


def finance_menu(message):
    try:
        if message.text == "💱 Курс валют":
            bot.send_message(message.from_user.id, '`Курс валют на сьогодні:\n\n{}`'.format(nbu_get_rate_info()),
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, finance_menu)
        elif message.text == "🔸 Назад":
            start(message)
    except TypeError as e:
        print("Wild Type Error occured! It uses \033[93m", e)
        print('\033[0m')
        pass


def tools_menu(message):
    try:
        if message.text == "🌦 Погода":

            keyboard = telebot.types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
            weatherTodayButton = telebot.types.KeyboardButton(text="🌦 На сьогодні")
            weatherTomorrowButton = telebot.types.KeyboardButton(text="🌦 На завтра")
            weatherFiveDaysButton = telebot.types.KeyboardButton(text="🌦 На 5 днів")
            returnButton = telebot.types.KeyboardButton(text="🔸 Назад")

            keyboard.add(weatherTodayButton, weatherTomorrowButton, weatherFiveDaysButton, returnButton)

            bot.send_message(message.from_user.id, '`Прогноз на сьогодні:\n' +
                             request_forecast_today(get_city_id("Kempen")) + "`",
                             parse_mode="Markdown",
                             reply_markup=keyboard)
            bot.register_next_step_handler(message, weather_menu)

        elif message.text == "📖 Пошук у Вікі":

            keyboard = telebot.types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
            returnButton = telebot.types.KeyboardButton(text="🔸 Ні, це все")
            keyboard.add(returnButton)
            bot.send_message(message.from_user.id, "Що мені пошукати у вікі? 📖",
                             parse_mode="Markdown",
                             reply_markup=keyboard)
            bot.register_next_step_handler(message, wiki_menu)

        elif message.text == "📝 Перекладач":

            keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            returnButton = telebot.types.KeyboardButton(text="🔸 Назад")
            keyboard.add(returnButton)

            bot.send_message(message.from_user.id, "Що мені перевести?",
                             parse_mode="Markdown",
                             reply_markup=keyboard)

            bot.register_next_step_handler(message, translate_menu_first)
        elif message.text == "🔸 Назад":
            start(message)
    except TypeError as e:
        print("Wild Type Error occured! It uses \033[93m", e)
        print('\033[0m')
        pass


def weather_menu(message):
    try:
        if message.text == "🌦 На сьогодні":
            bot.send_message(message.from_user.id, '`Прогноз на сьогодні:\n' +
                             request_forecast_today(get_city_id("Kempen")) + "`",
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, weather_menu)
        elif message.text == "🌦 На завтра":
            bot.send_message(message.from_user.id, '`Прогноз на завтра:\n' +
                             request_forecast_tomorrow(get_city_id("Kempen")) + "`",
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, weather_menu)
        elif message.text == "🌦 На 5 днів":
            bot.send_message(message.from_user.id, '`Прогноз на 5 днів:\n' +
                             request_forecast_five(get_city_id("Kempen")) + "`",
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, weather_menu)
        elif message.text == "🔸 Назад":
            tools_menu(message)
    except TypeError as e:
        print("Wild Type Error occured! It uses \033[93m", e)
        print('\033[0m')
        pass


def wiki_menu(message):
    if message.text != "🔸 Ні, це все":
        bot.send_message(message.from_user.id, "Ось що я знайшла:\n\n{}".format(wiki_search(message.text, "ru")),
                         parse_mode="Markdown")
        bot.send_message(message.from_user.id, "Що-небудь ще?",
                         parse_mode="Markdown")
        bot.register_next_step_handler(message, wiki_menu)
    elif message.text == "🔸 Ні, це все":
        start(message)


def translate_menu_first(message):

    if message.text == "🔸 Назад":
        start(message)

    else:
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        englishButton = telebot.types.KeyboardButton(text="🇬🇧 English")
        deutschButton = telebot.types.KeyboardButton(text="🇩🇪 German")
        ukrainianButton = telebot.types.KeyboardButton(text="🇺🇦 Ukrainian")
        russianButton = telebot.types.KeyboardButton(text="🇷🇺 Russian")
        returnButton = telebot.types.KeyboardButton(text="🔸 Отмена")
        keyboard.add(englishButton, deutschButton, ukrainianButton, russianButton, returnButton)

        fortranslate = message.text

        bot.send_message(message.from_user.id, "Якою мовою мені перекласти?",
                         parse_mode="Markdown",
                         reply_markup=keyboard)

        bot.register_next_step_handler(message, translate_menu_second, fortranslate)


def translate_menu_second(message, fortranslate):

    if message.text == "🔸 Назад":
        start(message)

    else:
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        returnButton = telebot.types.KeyboardButton(text="🔸 Назад")
        keyboard.add(returnButton)

        bot.send_message(message.from_user.id, translator.translate(fortranslate, dest=message.text[3:]).text,
                         parse_mode="Markdown")
        bot.send_message(message.from_user.id, "Що-небудь ще перекласти?",
                         parse_mode="Markdown",
                         reply_markup=keyboard)
        bot.register_next_step_handler(message, translate_menu_first)


@bot.message_handler(commands=['start'])
def start(message):
    try:
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        financeButton = telebot.types.KeyboardButton(text="💰 Фінанси")
        toolsButton = telebot.types.KeyboardButton(text="⚒ Інструменти")
        funButton = telebot.types.KeyboardButton(text="🎨 Розваги")
        keyboard.add(financeButton, toolsButton, funButton)
        bot.send_message(message.chat.id, "🔸 Меню", reply_markup=keyboard)
        bot.register_next_step_handler(message, menu)
    except TypeError as e:
        print("Wild Type Error occured! It uses \033[93m", e)
        print('\033[0m')
        pass


def assistant():
    bot.polling(none_stop=True, interval=0)


def timer():
    while True:
        schedule.run_pending()
        time.sleep(1)


schedule.every().day.at("08:00").do(morning_news)


if __name__ == '__main__':
    p1 = Process(target=assistant)
    p1.start()
    p2 = Process(target=timer)
    p2.start()
    p1.join()
    p2.join()
