#!/usr/bin/python
# -*- coding: utf-8
import telebot
import requests
import logging
from telebot import types
import sqlite3

# Экземпляр бота
bot = telebot.TeleBot('')

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


#
def get_db_connection():
    conn = sqlite3.connect('bot_database.db')
    return conn


@bot.message_handler(commands=['create'])
def create_user(message):
    msg = bot.reply_to(message, "Введите имя пользователя и возраст через пробел: ")
    bot.register_next_step_handler(msg, process_create_step)


def process_create_step(message):
    try:
        username, age = message.text.split()
        age = int(age)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, age) VALUES (?, ?)', (username, age))
        conn.commit()
        conn.close()
        bot.reply_to(message, "Пользователь успешно создан!")
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")


#
@bot.message_handler(commands=['read'])
def read_user(message):
    msg = bot.reply_to(message, "Введите имя пользователя для поиска: ")
    bot.register_next_step_handler(msg, process_read_step)


def process_read_step(message):
    try:
        username = message.text
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        if user:
            bot.reply_to(message, f"Пользователь: {user}")
        else:
            bot.reply_to(message, "Пользователь не найден.")
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")


#
@bot.message_handler(commands=['update'])
def update_user(message):
    msg = bot.reply_to(message, "Введите имя пользователя и новый возраст через пробел: ")
    bot.register_next_step_handler(msg, process_update_step)


def process_update_step(message):
    try:
        username, age = message.text.split()
        age = int(age)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        if user:
            cursor.execute('UPDATE users SET age = ? WHERE username = ?', (age, username))
            conn.commit()
            bot.reply_to(message, "Пользователь обновлен!")
        else:
            bot.reply_to(message, "Пользователь не найден.")
        conn.close()
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")


@bot.message_handler(commands=['delete'])
def delete_user(message):
    msg = bot.reply_to(message, "Введите имя пользователя для удаления")
    bot.register_next_step_handler(msg, process_delete_step)


def process_delete_step(message):
    try:
        username = message.text
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        if user:
            cursor.execute('DELETE FROM users WHERE username = ?', (username,))
            conn.commit()
            bot.reply_to(message, f"Пользователь {username} удален!")
        else:
            bot.reply_to(message, "Пользователь не найден.")
        conn.close()
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")


# Запуск бота
bot.polling()
