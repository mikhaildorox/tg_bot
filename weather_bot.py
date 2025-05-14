#!/usr/bin/python
# -*- coding: utf-8
import telebot
import requests
import logging
from telebot import types

# Экземпляр бота
bot = telebot.TeleBot('')

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


#
def get_weather(city):
    api_key = ''
    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'appid': api_key, 'units': 'metric'}
    response = requests.get(base_url, params)
    return response.json()


#
def process_weather_data(weather_data):
    if weather_data.get("cod") != 200:
        return "Город не найден"

    city = weather_data['name']
    weather = weather_data['weather'][0]['description']
    temperature = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    wind = weather_data['wind']['speed']

    return (f"Погода в {city}:\n"
            f"Описание {weather}\n"
            f"Температура: {temperature}\n"
            f"Влажность: {humidity}\n"
            f"Скорость ветра: {wind} м/с")


# Обработчик /start
@bot.message_handler(commands=['start'])
def start_command(message):
    try:
        # Логирование команды старт
        logger.info("Получена команда /start от пользователя %s", message.chat.id)
        # Попытка отправить приветственное сообщение пользователю
        bot.send_message(message.chat.id, "Добро пожаловать!")
        bot.reply_to(message, "Привет! Я твой Бот! Чем могу помочь?")

    except telebot.apihelper.ApiException as e:
        print(f"Ошибка при отправке сообщения: {e}")
        logger.error("Ошибка при отправке сообщения. Пожалуйста свяжите с поддержкой.")
        bot.send_message(message.chat.id, "Произошла ошибка при отправке сообщения. Попробуйте позже.")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        bot.send_message(message.chat.id, "Произошла неизвестная ошибка. Свяжитесь с поддержкой.")
    else:
        print("Сообщение отправлено.")
        logger.info("Сообщение успешно отправлено пользователю %s", message.chat.id)
    finally:
        print("Завершение работы команды /start")
        logger.info("Завершение обработки команды /start для пользователя %s", message.chat.id)


@bot.message_handler(commands=['help', 'about'])
def help_command(message):
    bot.reply_to(message, "Раздел помощи. Информация о Боте")


#
@bot.message_handler(commands=['weather'])
def send_city(message):
    bot.send_message(message.chat.id, "Введите название города, чтобы узнать погоду.")


@bot.message_handler(func=lambda message: True)
def send_weather(message):
    city = message.text
    weather_data = get_weather(city)
    weather_message = process_weather_data(weather_data)
    bot.send_message(message.chat.id, weather_message)


# Запуск бота
bot.polling()
