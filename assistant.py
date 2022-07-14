import telebot
from WeatherForecast import *
from BankAccounting import *
from RandomFact import *
from SearchWikipedia import *
from googletrans import Translator

bot = telebot.TeleBot(config.botToken)
translator = Translator()


def menu(message):
    try:
        if message.text == "💰 Финансы":

            keyboard = telebot.types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
            exchangeButton = telebot.types.KeyboardButton(text="💱 Курс валют")
            returnButton = telebot.types.KeyboardButton(text="🔸 Назад")
            keyboard.add(exchangeButton, returnButton)
            bot.send_message(message.chat.id,
                             text="💸 Финансовый уголок\n\n{}".format(mono_get_client_info()),
                             parse_mode="Markdown",
                             reply_markup=keyboard)
            bot.register_next_step_handler(message, finance_menu)

        elif message.text == "⚒ Инструменты":

            keyboard = telebot.types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
            weatherButton = telebot.types.KeyboardButton(text="🌦 Погода")
            wikipediaButton = telebot.types.KeyboardButton(text="📖 Поиск в Вики")
            translateButton = telebot.types.KeyboardButton(text="📝 Переводчик")
            returnButton = telebot.types.KeyboardButton(text="🔸 Назад")
            keyboard.add(weatherButton, wikipediaButton, translateButton, returnButton)
            bot.send_message(message.chat.id, text="🔸 Панель инструментов",
                             parse_mode="Markdown",
                             reply_markup=keyboard)

            bot.register_next_step_handler(message, tools_menu)

        elif message.text == "🎨 Досуг":

            keyboard = telebot.types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
            returnButton = telebot.types.KeyboardButton(text="🔸 Назад")
            keyboard.add(returnButton)

            bot.send_message(message.chat.id, text="Здесь пока ничего нет",
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
            bot.send_message(message.from_user.id, '`Курс валют на сегодня:\n\n{}`'.format(nbu_get_rate_info()),
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
            weatherTodayButton = telebot.types.KeyboardButton(text="🌦 На сегодня")
            weatherTomorrowButton = telebot.types.KeyboardButton(text="🌦 На завтра")
            weatherFiveDaysButton = telebot.types.KeyboardButton(text="🌦 На 5 дней")
            returnButton = telebot.types.KeyboardButton(text="🔸 Назад")

            keyboard.add(weatherTodayButton, weatherTomorrowButton, weatherFiveDaysButton, returnButton)

            bot.send_message(message.from_user.id, '`Прогноз на сегодня:\n' +
                             request_forecast_today(get_city_id("Kempen")) + "`",
                             parse_mode="Markdown",
                             reply_markup=keyboard)
            bot.register_next_step_handler(message, weather_menu)

        elif message.text == "📖 Поиск в Вики":

            keyboard = telebot.types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
            returnButton = telebot.types.KeyboardButton(text="🔸 Нет, это всё")
            keyboard.add(returnButton)
            bot.send_message(message.from_user.id, "Что мне поискать в Википедии? 📖",
                             parse_mode="Markdown",
                             reply_markup=keyboard)
            bot.register_next_step_handler(message, wiki_menu)

        elif message.text == "📝 Переводчик":

            keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            returnButton = telebot.types.KeyboardButton(text="🔸 Отмена")
            keyboard.add(returnButton)

            bot.send_message(message.from_user.id, "Что мне перевести?",
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
        if message.text == "🌦 На сегодня":
            bot.send_message(message.from_user.id, '`Прогноз на сегодня:\n' +
                             request_forecast_today(get_city_id("Kempen")) + "`",
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, weather_menu)
        elif message.text == "🌦 На завтра":
            bot.send_message(message.from_user.id, '`Прогноз на завтра:\n' +
                             request_forecast_tomorrow(get_city_id("Kempen")) + "`",
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, weather_menu)
        elif message.text == "🌦 На 5 дней":
            bot.send_message(message.from_user.id, '`Прогноз на 5 дней:\n' +
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
    if message.text != "🔸 Нет, это всё":
        bot.send_message(message.from_user.id, "Вот что я нашла:\n\n{}".format(wiki_search(message.text, "ru")),
                         parse_mode="Markdown")
        bot.send_message(message.from_user.id, "Что-нибудь ещё?",
                         parse_mode="Markdown")
        bot.register_next_step_handler(message, wiki_menu)
    elif message.text == "🔸 Нет, это всё":
        start(message)


def translate_menu_first(message):

    if message.text == "🔸 Отмена":
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

        bot.send_message(message.from_user.id, "На какой язык мне перевести?",
                         parse_mode="Markdown",
                         reply_markup=keyboard)

        bot.register_next_step_handler(message, translate_menu_second, fortranslate)


def translate_menu_second(message, fortranslate):

    if message.text == "🔸 Отмена":
        start(message)

    else:
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        returnButton = telebot.types.KeyboardButton(text="🔸 Отмена")
        keyboard.add(returnButton)

        bot.send_message(message.from_user.id, translator.translate(fortranslate, dest=message.text[3:]).text,
                         parse_mode="Markdown")
        bot.send_message(message.from_user.id, "Что-нибудь ещё перевести?",
                         parse_mode="Markdown",
                         reply_markup=keyboard)
        bot.register_next_step_handler(message, translate_menu_first)


@bot.message_handler(commands=['start'])
def start(message):
    try:
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        financeButton = telebot.types.KeyboardButton(text="💰 Финансы")
        toolsButton = telebot.types.KeyboardButton(text="⚒ Инструменты")
        funButton = telebot.types.KeyboardButton(text="🎨 Досуг")
        keyboard.add(financeButton, toolsButton, funButton)
        bot.send_message(message.chat.id, "🔸 Меню", reply_markup=keyboard)
        bot.register_next_step_handler(message, menu)
    except TypeError as e:
        print("Wild Type Error occured! It uses \033[93m", e)
        print('\033[0m')
        pass


bot.polling(none_stop=True, interval=0)
