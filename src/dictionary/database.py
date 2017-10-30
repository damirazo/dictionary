# coding: utf-8
import sqlite3
from contextlib import contextmanager


def raw_connection():
    """
    "Сырое" соединение с БД с необходимостью ручного коммита и закрытия
    """
    from dictionary.views import app

    return sqlite3.connect(app.config['DATABASE_PATH'])


@contextmanager
def connection():
    """
    Менеджер контекста, формирующий курсор к СУБД
    """
    from dictionary.views import app

    db = sqlite3.connect(app.config['DATABASE_PATH'])
    yield db.cursor()
    db.commit()
    db.close()


def row_by_key(key):
    """
    Получаем значение из СУБД с заданным ключом

    :param key: Ключ элемента
    :type key: str
    :rtype: tuple or None
    """
    with connection() as c:
        c.execute('SELECT key, value FROM dict WHERE key = ?', (key,))
        data = c.fetchone()

    return data


def has_row_by_key(key):
    u"""
    Проверка наличия записи с указанным ключем

    :param key: Ключ элемента
    :type key: str
    :rtype: bool
    """
    return row_by_key(key) is not None


def add_row(key, value):
    u"""
    Добавление новой записи с указанным ключем и значением

    :param key: Ключ элемента
    :type key: str
    :param value: Значение элемента
    :type value: str
    """
    with connection() as c:
        c.execute("INSERT INTO dict (key, value) VALUES (?, ?)", (key, value))


def update_row(key, value):
    u"""
    Обновление значения элемента с указанным ключом

    :param key: Ключ элемента
    :type key: str
    :param value: Значение элемента
    :type value: str
    """
    with connection() as c:
        c.execute("UPDATE dict SET value = ? WHERE key = ?", (value, key))


def delete_row(key):
    u"""
    Удаление записи с указанным ключем

    :param key: Ключ элемента
    :type key: str
    """
    with connection() as c:
        c.execute("DELETE FROM dict WHERE key = ?", (key,))
