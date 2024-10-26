import sqlite3

connect = sqlite3.connect("bot_data.db")
cursor = connect.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users_table(user_id INTEGER PRIMARY KEY UNIQUE, full_name TEXT, joined_date TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS kitoblar(path TEXT)")

