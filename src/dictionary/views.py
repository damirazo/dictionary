from flask import Flask, abort, request, jsonify
from dictionary.database import row_by_key, add_row, update_row, delete_row
from dictionary.helpers import parse_request, get_time

__all__ = ['app']


app = Flask(__name__)


@app.route('/dictionary/<key>', methods=['GET'])
def request_get(key):
    """
    Получение записи по ключу
    """
    row = row_by_key(key)
    if row is None:
        return abort(404)
    else:
        key, value = row

    return jsonify({'key': key, 'value': value, 'time': get_time()})


@app.route('/dictionary', methods=['POST'])
def request_post():
    """
    Добавление новой записи
    """
    data = parse_request(request.data, context_keys=('key', 'value'))
    if data is None:
        return abort(400)

    key = data['key']
    value = data['value']

    row = row_by_key(key)
    if row is not None:
        return abort(409)

    add_row(key, value)

    return jsonify({'key': key, 'value': value, 'time': get_time()})


@app.route('/dictionary/<key>', methods=['PUT'])
def request_put(key):
    """
    Обновление записи
    """
    row = row_by_key(key)
    if row is None:
        return abort(404)

    data = parse_request(request.data, context_keys=('value',))
    if data is None:
        return abort(400)

    value = data['value']

    update_row(key, value)

    return jsonify({'key': key, 'value': value, 'time': get_time()})


@app.route('/dictionary/<key>', methods=['DELETE'])
def request_delete(key):
    """
    Удаление записи
    """
    delete_row(key)

    return ''
