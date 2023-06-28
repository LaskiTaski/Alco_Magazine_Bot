import sqlite3 as sq


def plus(name):
    """
    Добавляет +1 выбранный товар в БД пользователя.
    :param name: Название товара который хотим добавить.
    """
    base = sq.connect('magazine.dp')
    try:
        cur = base.cursor()
        cur.execute(f"SELECT Количество FROM alcohol WHERE Название='{name}'")
        result = cur.fetchone()[0]
        result -= 1
        cur.execute(f"UPDATE alcohol set Количество= {result} WHERE Название='{name}'")
        base.commit()
        print(f"plus ------> Other✓")
    except sq.Error as error:
        print(f"PLUS ERROR {error} ------> OTHER -----------------------> OTHER")


def minus(name):
    """
    Добавляет +1 выбранный товар в БД пользователя.
    :param name: Название товара который хотим добавить.
    """
    base = sq.connect('magazine.dp')
    try:
        cur = base.cursor()
        cur.execute(f"SELECT Количество FROM alcohol WHERE Название='{name}'")
        result = cur.fetchone()[0]
        result += 1
        cur.execute(f"UPDATE alcohol set Количество= {result} WHERE Название='{name}'")
        base.commit()
        print(f"minus ------> Other✓")
    except sq.Error as error:
        print(f"MINUS ERROR {error} ------> OTHER -----------------------> OTHER")


def read(name):
    """
    :param name: Название искомого товара для получения количества.
    :return: Возвращает кол-во товара на складе.
    """
    base = sq.connect('magazine.dp')
    try:
        cur = base.cursor()
        cur.execute(f"SELECT Количество FROM alcohol WHERE Название='{name}'")
        records = cur.fetchone()
        base.close()
        print(f"read ------> Other✓")
        return records

    except sq.Error as error:
        print(f"READ ERROR {error} ------> OTHER -----------------------> OTHER")
