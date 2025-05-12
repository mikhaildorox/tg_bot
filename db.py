#!/usr/bin/python
# -*- coding: utf-8

import sqlite3

# создание подключения
conn = sqlite3.connect("database.db")

# создание курсора для SQL-запросов
cursor = conn.cursor()

# создание базы данных
cursor.execute("""
CREATE TABLE users (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL
)
""")

# сохранение изменений и закрытие соезинения
conn.commit()
conn.close()
