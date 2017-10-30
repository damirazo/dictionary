# coding: utf-8
import json


def parse_request(data, context_keys):
    u"""
    Пробуем распарсить запрос
    Нас интересуют параметры с именами key и value
    """
    if not data:
        return

    dct = json.loads(data.decode('utf-8'))
    if not all(k in dct for k in context_keys):
        return

    return dct
