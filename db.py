import sqlite3

DB_PATH = 'db/hdd-nsa-bot.sqlite'

db_conn = None
db_cur = None

def db_connect():

    global db_conn, db_cur

    try:
        db_conn = sqlite3.connect(DB_PATH)
        db_cur = db_conn.cursor()
        print("Подключение к sqlite выполнено")

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)


def db_close():
    global db_conn, db_cur

    if (db_conn):
        db_cur.close()
        db_conn.close()
        print("База sqlite закрыта")


def insert_user(user):
    #print(user)
    global db_conn, db_cur

    db_connect()

    try:
        params = (user['id'], user['username'], user['first_name'], user['last_name'])
        q = 'REPLACE INTO users(id, username, first_name, last_name) VALUES(?, ?, ?, ?)'

        db_cur.execute(q, params)
        db_conn.commit()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)

    db_close()


