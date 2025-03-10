import sqlite3

connect = sqlite3.connect("bot_data.db")
cursor = connect.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS users_table(user_id INTEGER PRIMARY KEY UNIQUE, full_name TEXT, joined_date TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS kitoblar(path TEXT)")
cursor.execute(
    "CREATE TABLE IF NOT EXISTS user_full_data(ism TEXT NULL, tg_id TEXT UNIQUE NULL,phone_number TEXT NULL,joined_data TEXT NULL)")
cursor.execute("""CREATE TABLE IF NOT EXISTS payments_data(ism TEXT NULL, tg_id TEXT NULL, transaction_id TEXT UNIQUE NULL, summa TEXT DEFAULT "100.000", joined_date datetime NULL, lefted_date datetime NULL, status_joined BOOLEAN DEFAULT 1)""")



async def add_payment_data(ism,tg_id,transaction_id,joined_date,lefted_date):
    cursor.execute("INSERT INTO payments_data (ism,tg_id,transaction_id,joined_date,lefted_date) VALUES (?, ?, ?, ?, ?)",(ism,tg_id,transaction_id,joined_date,lefted_date))
    connect.commit()

async def get_expired_users(current_date):
    cursor.execute("SELECT tg_id FROM payments_data WHERE lefted_date <= ? AND status_joined == 1",(current_date,))
    expired_users = cursor.fetchall()
    return [user[0] for user in expired_users]

async def update_payment_data(tg_id):
    cursor.execute("UPDATE payments_data SET status_joined = 0 WHERE tg_id = ?",(tg_id,))
    connect.commit()

async def check_user_data(tg_id):
    cursor.execute('SELECT * FROM user_full_data WHERE tg_id=?', (tg_id,))
    if cursor.fetchone():
        return True
    else:
        return False

async def get_name_user(tg_id):
    cursor.execute('SELECT ism FROM user_full_data WHERE tg_id=?', (tg_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    return None
        


async def bazaga_qoshish(ism, tg_id, joined_data):
    cursor.execute('SELECT * FROM user_full_data WHERE tg_id=?', (tg_id,))
    if cursor.fetchone():
        return True
    else:
        cursor.execute("INSERT INTO user_full_data (ism, tg_id, joined_data) VALUES (?, ?, ?)",
                       (ism, tg_id, joined_data))
        connect.commit()
        return f"{ism} siz ro`yxatdan o`tdingiz\ntelefon raqamingizni pastdagi tugma orqali jo`nating"


async def update_contact(tg_id, phone_number):
    cursor.execute('SELECT * FROM user_full_data WHERE tg_id=?', (tg_id,))
    if cursor.fetchone():
        cursor.execute('UPDATE user_full_data SET phone_number=? WHERE tg_id=?', (phone_number, tg_id))
        connect.commit()
        return True
    else:
        return False




def get_all_data():
    cursor.execute('SELECT * FROM user_full_data')
    return cursor.fetchall()