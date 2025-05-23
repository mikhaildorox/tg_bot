#!/usr/bin/python
# -*- coding: utf-8
import telebot
import logging
from telebot import types
import requests

from db import cursor

# Экземпляр бота
bot = telebot.TeleBot('')

url = "https://catfact.ninja/fact"

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Обработчик /start
@bot.message_handler(commands=['start'])
def start_command(message):
    try:
        # Логирование команды старт
        logger.info("Получена команда /start от пользователя %s", message.chat.id)
        # Попытка отправить приветственное сообщение пользователю
        bot.send_message(message.chat.id, "Добро пожаловать!")
        bot.reply_to(message, "Привет! Я твой Бот! Чем могу помочь?")

        # Клавиатура с двумя кнопками
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

        # Создание кнопок с callback-данными
        button1 = types.KeyboardButton('CatFact')
        button2 = types.KeyboardButton('Кнопка 2')

        # # Клавиатура с двумя кнопками
        # keyboard = types.InlineKeyboardMarkup(row_width=2)
        #
        # # Создание кнопок с callback-данными
        # button1 = types.InlineKeyboardButton('Кнопка 1', callback_data='data1')
        # button2 = types.InlineKeyboardButton('Кнопка 2', callback_data='data2')

        # Добавление кнопок на клавиатуру
        keyboard.add(button1, button2)

        # Отправление сообщений с клавиатуры
        bot.send_message(message.chat.id, "Выберите опцию: ", reply_markup=keyboard)
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


# Отправка и получение изображений, видео и документов.
@bot.message_handler(content_types=['photo'])
def handler_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open("received_image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, "Изображение получено и сохранено")


# отправка изображения в ответ на команду /sendphoto
@bot.message_handler(commands=['sendphoto'])
def send_photo(message):
    photo = open('received_image.jpg', 'rb')
    # photo = open('path_to_your_image.jpg', 'rb')
    bot.send_photo(message.chat.id, photo)


# Обработка видео
@bot.message_handler(content_types=['video'])
def handler_video(message):
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open("received_video.mp4", 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, "Видео получено и сохранено")


# отправка видео в ответ на команду /sendvideo
@bot.message_handler(commands=['sendvideo'])
def send_video(message):
    video = open('received_video.mp4', 'rb')
    bot.send_photo(message.chat.id, video)


# Обработка документа
@bot.message_handler(content_types=['document'])
def handler_document(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open(message.document.file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, "Документ получен и сохранен")


# отправка документа в ответ на команду /senddocument
@bot.message_handler(commands=['senddocument'])
def send_document(message):
    document = open('Полиморфизм.txt', 'rb')
    bot.send_document(message.chat.id, document)


# Обработчик тестовых сообщений
@bot.message_handler(content_types=['text'])
def handler_text(message):
    response = f"Ваш текст: {message.text}"
    bot.send_message(message.chat.id, response)


#  клавиатура inline
@bot.callback_query_handler(func=lambda call: True)
def handler_query(call):
    # Проверяем callback-данные и отправляем ответ
    if call.data == "data1":
        bot.send_message(call.message.chat.id, "НАЖАТА кнопка 1")
    elif call.data == "data2":
        bot.send_message(call.message.chat.id, "НАЖАТА кнопка 2")


# Клавиатура Reply
@bot.message_handler(content_types=['text'])
def handler_text(message):
    # Проверяем текст сообщения и отправляем ответ
    if message.text == "CatFact":
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            bot.send_message(message.chat.id, str(data["fact"]))
        else:
            bot.send_message(message.chat.id, f"Ошибка: {response.status_code}")
    elif message.text == "Кнопка 2":
        bot.send_message(message.chat.id, "Вы НАЖАЛИ кнопку 2")


# Запуск бота
bot.polling()
