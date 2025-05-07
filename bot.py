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

# Запуск бота
bot.polling()
