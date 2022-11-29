import sqlite3

DB_PATH = 'db/hdd-nsa-bot.sqlite'


def db_connect():
    try:
        conn = sqlite3.connect(DB_PATH)
        print("Подключение к sqlite выполнено")
        return conn

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)


def db_close():
    if (db_conn):
        db_cur.close()
        db_conn.close()
        print("База sqlite закрыта")


def insert_user(user):
    #print(user)
    try:
        params = (user['id'], user['username'], user['first_name'], user['last_name'])
        q = 'REPLACE INTO users(id, username, first_name, last_name) VALUES(?, ?, ?, ?)'

        db_cur.execute(q, params)
        db_conn.commit()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)


db_conn = db_connect()
db_cur = db_conn.cursor()
