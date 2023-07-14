import sqlite3 as sq


def create():
    """
    Создание БД для пользователя.
    """
    try:
        base = sq.connect('magazine.dp')
        print("Загрузка данных для пользователя...")
        if base:
            base.execute('CREATE TABLE IF NOT EXISTS information_base('
                         'Пользователь TEXT,'
                         'Название TEXT,'
                         'Количество INTEGER,'
                         'Цена INTEGER,'
                         'Общая INTEGER)'
                         )
        base.commit()
        base.close()
        print(f"create ------> client✓")
    except sq.Error as error:
        print(f"CREATE ERROR {error} ------> CLIENT -----------------------> CLIENT")


async def add(info: list):
    """
    Добавление информации о заказе клиента.
    :param info: Имя пользователя, Название товара, Количество, Цена за шт, Общая цена.
    """
    base = sq.connect('magazine.dp')
    try:
        cur = base.cursor()
        cur.execute('INSERT OR IGNORE INTO information_base VALUES (?, ?, ?, ?, ?)', tuple(info))
        base.commit()
        base.close()
        print(f"add ------> client✓")
    except sq.Error as error:
        print(f"ADD ERROR {error} ------> CLIENT -----------------------> CLIENT")


async def updata(key: str, value: (int, float), product: str):
    """
    Обновление данных о заказе пользователя.
    :param key: Что меняем Количество/Общая цена.
    :param value: Значение на которе меняем информацию из ячейки.
    :param product: Название продукта.
    """
    base = sq.connect('magazine.dp')
    try:
        cur = base.cursor()
        if key == 'Количество':
            request = f"UPDATE information_base set 'Количество'= ? WHERE Название='{product}'"
        else:
            request = f"UPDATE information_base set 'Общая'= ? WHERE Название='{product}'"
        data = (value,)
        cur.execute(request, data)
        base.commit()
        base.close()
        print(f"update ------> client✓")
    except sq.Error as error:
        print(f"UPDATE ERROR {error} ------> CLIENT -----------------------> CLIENT")


def in_the_table(user, product, quanti):
    base = sq.connect('magazine.dp')
    try:
        cur = base.cursor()
        cur.execute(f"SELECT * FROM information_base "
                    f"WHERE Название='{product}' AND "
                    f"Пользователь='{user}' AND "
                    f"Количество='{quanti}'")
        records = cur.fetchall()
        base.close()
        print(f"in the table ------> client✓")
        return records

    except sq.Error as error:
        print(error)
        print(f"IN THE TABLE {product} НЕ НАЙДЕННО ------> CLIENT -----------------------> CLIENT")


def read(name: str):
    """
    Считывание кол-ва товаров по названию в БД для пользователя.
    :param name: Название товара который ищем.
    :return: Количество товара в БД.
    """
    base = sq.connect('magazine.dp')
    try:
        cur = base.cursor()
        cur.execute(f"SELECT Количество FROM information_base WHERE Название='{name}'")
        records = cur.fetchone()
        base.close()
        print(f"read ------> client✓")
        return records

    except sq.Error as error:
        print(name)
        print(f"READ ERROR {error} ------> CLIENT -----------------------> CLIENT")


def check(id):
    """
    Выгрузка данных о заказе пользователя.
    :param id: ID пользователя.
    :return: ВЕСЬ ЗАКАЗ ПОЛЬЗОВАТЕЛЯ
    """

    base = sq.connect('magazine.dp')
    try:
        cur = base.cursor()
        cur.execute(f"SELECT Название, Количество, Общая FROM information_base WHERE Пользователь='{id}'")
        result = cur.fetchall()
        text = ''
        name = [' \n', 'шт.', 'руб.']
        summa = 0
        for product in result:
            if product[1] != 0:
                for k, v in zip(product, name):
                    if v == 'руб.':
                        k = round(k, 2)
                        summa += k

                    text += str(k) + v + '     '
                text += '\n\n'
        text += f'Общая сумма: {round(summa, 2)}'

        base.close()
        print(f"check ------> client✓")
        return [text, summa]

    except sq.Error as error:
        print(f"CHECK ERROR {error} ------> CLIENT -----------------------> CLIENT")
