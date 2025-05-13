#!/usr/bin/python
# -*- coding: utf-8

import sqlite3

# создание подключения
conn = sqlite3.connect("bot_database.db")

# создание курсора для SQL-запросов
cursor = conn.cursor()

# создание базы данных
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    age INTEGER
)
""")

# сохранение изменений и закрытие соезинения
conn.commit()
conn.close()
