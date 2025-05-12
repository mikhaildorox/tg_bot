import sqlite3

# Создание или подключение к БД
conn = sqlite3.connect("database.db")

# Создание курсора для выполнения SQL-запросов
cursor = conn.cursor()

# Пример создания таблицы
cursor.execute("""
CREATE TABLE users (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL
)
""")

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()