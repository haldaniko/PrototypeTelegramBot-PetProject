import requests
import random
from datetime import datetime


def get_today_fact():
    try:
        fact = requests.get("http://numbersapi.com/{}/{}/date".
                            format(datetime.now().month, datetime.now().day)).text
        return fact
    except Exception as e:
        print("Exception :", e)
        pass


def get_number_fact():
    try:
        fact = requests.get("http://numbersapi.com/{}/trivia/".
                            format(random.randrange(0, 100))).text
        return fact
    except Exception as e:
        print("Exception :", e)
        pass


def get_random_joke():
    try:
        joke = requests.get("https://geek-jokes.sameerkumar.website/api?format=json:").text
        return joke
    except Exception as e:
        print("Exception:", e)
        pass


def get_random_quote(language):
    try:
        res = requests.get("https://api.fisenko.net/v1/quotes/{}/random".format(language))
        data = res.json()
        quote = "{}\n© {}".format(data['text'], data['author']['name'])
        return quote
    except Exception as e:
        print("Exception:", e)
        pass


def get_news_ukraine():
    try:
        res = requests.get("https://newsapi.org/v2/top-headlines?country=ua&apiKey=0ecaf71321e54e8d95c90abd69fcbafb")
        data = res.json()
        return data
    except Exception as e:
        print("Exception:", e)
        pass

