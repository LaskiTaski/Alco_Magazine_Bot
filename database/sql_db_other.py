import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('magazine.dp')
    cur = base.cursor()
    print("Product data uploaded...")
    if base:
        base.execute('CREATE TABLE IF NOT EXISTS alcohol('
                     'Раздел TEXT,'
                     'Название TEXT,'
                     'Цена INTEGER,'
                     'Описание TEXT,'
                     'Склад INTEGER)'
                     )
    base.commit()


def sql_add(line):
    cur.execute('INSERT OR IGNORE INTO alcohol VALUES (?, ?, ?, ?, ?)', tuple(line))
    base.commit()


def sql_gen_chapter():
    cur.execute("SELECT Раздел FROM alcohol")
    result = set(cur.fetchall())
    return result


def sql_gen_name(name):
    cur.execute(f"SELECT Название FROM alcohol WHERE Раздел='{name}'")
    result = set(cur.fetchall())
    return result

def sql_gen_info(name):
    cur.execute(f"SELECT Цена, Описание, Склад FROM alcohol WHERE Название='{name}'")
    result = cur.fetchone()
    return result

def sql_plus(name):
    cur.execute(f"SELECT Склад FROM alcohol WHERE Название='{name}'")
    result = cur.fetchone()[0]-1
    cur.execute(f"UPDATE alcohol set Склад= {result} WHERE Название='{name}'")
    print(f'{result} Значение из таблицы')
