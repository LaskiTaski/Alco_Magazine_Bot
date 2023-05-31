import sqlite3 as sq

def sql_start():
    global base, cur
    base = sq.connect('magazine.dp')
    cur = base.cursor()
    print("Database created...")
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

