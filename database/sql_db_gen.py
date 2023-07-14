import sqlite3 as sq


def create():
    """
    Создание БД с Товарами.
    """
    global base, cur
    base = sq.connect('magazine.dp')
    try:
        cur = base.cursor()
        print(f"create ------> gen...")
        if base:
            base.execute('CREATE TABLE IF NOT EXISTS alcohol('
                         'Раздел TEXT,'
                         'Название TEXT,'
                         'Цена INTEGER,'
                         'Описание TEXT,'
                         'Количество INTEGER)'
                         )
        base.commit()
        base.close()
        print(f"create ------> gen✓")
    except sq.Error as error:
        print(f"CREATE ERROR {error} ------> GEN")


def add(line: list):
    """
    Добавляет информацию о товарах.
    :param line: Список информации о товаре.
    """
    base = sq.connect('magazine.dp')
    try:
        cur = base.cursor()
        cur.execute('INSERT OR IGNORE INTO alcohol VALUES (?, ?, ?, ?, ?)', tuple(line))
        base.commit()
        base.close()
    except sq.Error as error:
        print(f"ADD ERROR {error} ------> GEN")


def chapter():
    """
    Заполняет разделы БД.
    """
    base = sq.connect('magazine.dp')
    try:
        cur = base.cursor()
        cur.execute("SELECT Раздел FROM alcohol")
        result = set(cur.fetchall())
        base.commit()
        base.close()
        print(f"generation ------> chapter✓")
        return result
    except sq.Error as error:
        print(f"GENERATION ------> CHAPTER ERROR {error} ------> GEN -----------------------> GEN")


def name(name: str):
    """
    Заполняет Названия товаров по разделам.
    :param name: Название раздела.
    """
    base = sq.connect('magazine.dp')
    try:
        cur = base.cursor()
        cur.execute(f"SELECT Название FROM alcohol WHERE Раздел='{name}'")
        result = set(cur.fetchall())
        base.commit()
        base.close()
        print(f"generation ------> name✓")
        return result
    except sq.Error as error:
        print(f"GENERATION ------> NAME ERROR {error} ------> GEN -----------------------> GEN")


def info(name):
    """
    Выдаёт полную информацию о товаре.
    :param name: Название товара.
    :return: Цена, Описание, Количество.
    """
    base = sq.connect('magazine.dp')
    try:
        cur = base.cursor()
        cur.execute(f"SELECT Цена, Описание, Количество FROM alcohol WHERE Название='{name}'")
        result = cur.fetchone()
        base.commit()
        base.close()
        print(f"generation ------> INFO✓")
        return result
    except sq.Error as error:
        print(f"GENERATION ------> INFO ERROR {error} ------> GEN -----------------------> GEN")
