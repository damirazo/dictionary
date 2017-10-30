# coding: utf-8
import datetime
import json


def parse_request(data, context_keys):
    """
    Пробуем распарсить запрос
    Нас интересуют параметры с именами key и value
    """
    if not data:
        return

    dct = json.loads(data.decode('utf-8'))
    if not all(k in dct for k in context_keys):
        return

    return dct


def get_time():
    """
    Текущая дата и время в формате ГГГГ-мм-ДД ЧЧ:ММ
    """
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
