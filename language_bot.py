import telebot
import sqlite3

from db import cursor

bot = telebot.TeleBot('')

conn = sqlite3.connect('language_helper.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS phrases (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        word TEXT UNIQUE,
                        translation TEXT,
                        example TEXT)
''')

conn.commit()

phrases = [
    ("hello", "привет", "Hello! How are you?"),
    ("goodbye", "пока", "Goodbye! See you later.")
]

cursor.executemany('INSERT OR IGNORE INTO phrases (word, translation, example) VALUES (?, ?, ?)', phrases)
conn.commit()

def get_random_phrase():
    cursor.execute('SELECT id, word, translation, example FROM phrases ORDER BY RANDOM() LIMIT 1')
    return cursor.fetchone()


def add_phrase(word, translation, example):
    cursor.execute("INSERT INTO phrases (word, translation, example) VALUES (?, ?, ?)", (word, translation, example))
    conn.commit()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
                 "Привет! Я Language Helper"
                 "Отправь команду /phrase, чтобы получить случайное слово или фразу для изучения."
                 "Отправь команду /add слово, перевод, пример, чтобы добавить новую фразу.")


@bot.message_handler(commands=['add'])
def add_phrase(message):
    try:
        parts = message.text[len('/add '):].split(',')
        if len(parts) != 3:
            raise ValueError('Неверное количество аргументов')

        word, translation, example = map(str.strip, parts)

        add_phrase(word, translation, example)
        bot.reply_to(message, f"Фраза {word} успешно добавлена")
    except ValueError:
        bot.reply_to(message, "Пожалуйста, используйте формат: /add слово, перевод, пример")


@bot.message_handler(commands=['phrase'])
def send_phrase(message):
    phrase = get_random_phrase()
    id, word, translation, example = phrase

    phrase_message = (f"Слово: {word}\n"
                      f"Перевод: {translation}\n"
                      f"Пример: {example}")

    bot.reply_to(message, phrase_message)

bot.infinity_polling()