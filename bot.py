#!/usr/bin/python
# -*- coding: utf-8
import telebot

# Экземпляр бота
bot = telebot.TeleBot('')


# Обработчик /start
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "Привет! Я твой Бот! Чем могу помочь?")


# Запуск бота
bot.polling()
