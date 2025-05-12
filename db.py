import sqlite3

# �������� ��� ����������� � ��
conn = sqlite3.connect("database.db")

# �������� ������� ��� ���������� SQL-��������
cursor = conn.cursor()

# ������ �������� �������
cursor.execute("""
CREATE TABLE users (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL
)
""")

# ���������� ��������� � �������� ����������
conn.commit()
conn.close()