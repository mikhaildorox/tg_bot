#!/usr/bin/python
# -*- coding: utf-8
import telebot

# Экземпляр бота
bot = telebot.TeleBot('')


# Обработчик /start
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "Привет! Я твой Бот! Чем могу помочь?")


@bot.message_handler(commands=['help', 'about'])
def help_command(message):
    bot.reply_to(message, "Раздел помощи. Информация о Боте")


# Обработчик тестовых сообщений
@bot.message_handler(content_types=['text'])
def handler_text(message):
    response = f"Ваш текст: {message.text}"
    bot.send_message(message.chat.id, response)


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
    photo = open('path_to_your_image.jpg', 'rb')
    bot.send_photo(message.chat.id, photo)

# Запуск бота
bot.polling()
