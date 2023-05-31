import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('magazine.dp')
    cur = base.cursor()
    if base:
        base.execute('CREATE TABLE IF NOT EXISTS settings('
                     'Раздел TEXT,'
                     'Название TEXT,'
                     'Цена INTEGER,'
                     'Описание TEXT,'
                     'Склад INTEGER)'
                     )
        print('Таблица создана')
    base.commit()


def sql_add_command_admin(line):
    cur.execute('INSERT OR IGNORE INTO settings VALUES (?, ?, ?, ?, ?)', tuple(line))
    base.commit()
