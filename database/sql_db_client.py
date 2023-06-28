import sqlite3 as sq


def sql_start_client():
    global base, cur
    base = sq.connect('magazine.dp')
    cur = base.cursor()
    print("User data uploaded...")
    if base:
        base.execute('CREATE TABLE IF NOT EXISTS information_base('
                     'Пользователь TEXT,'
                     'Товар TEXT,'
                     'Количество INTEGER,'
                     'Цена INTEGER,'
                     'Общая INTEGER)'
                     )
    base.commit()


async def sql_add_client(info):
    cur.execute('INSERT OR IGNORE INTO information_base VALUES (?, ?, ?, ?, ?)', tuple(info))
    base.commit()


async def sql_update_client(key,value,product):
    try:
        cursor = base.cursor()
        if key == 'Количество':
            sql_request = f"UPDATE information_base set 'Количество' = ? WHERE Товар='{product}'"
        else:
            sql_request = f"UPDATE information_base set 'Общая' = ? WHERE Товар='{product}'"
        data = (value,)
        cursor.execute(sql_request, data)
        base.commit()
    except sq.Error as error:
        print("Update sq ERROR", error)


def sql_read_client(name):
    try:
        cursor = base.cursor()
        sqlite_select_query = f"SELECT Количество FROM information_base WHERE Товар='{name}'"
        cursor.execute(sqlite_select_query)
        records = cursor.fetchone()
        return records

    except sq.Error as error:
        print("Read sq ERROR", error)

# Выдать чек 
def sql_drop_check(name):
    try:
        cursor = base.cursor()
        sqlite_select_query = f"SELECT * FROM information_base"
        cursor.execute(sqlite_select_query)
        records = cursor.fetchone()
        return records

    except sq.Error as error:
        print("Read sq ERROR", error)