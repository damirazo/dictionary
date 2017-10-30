# coding: utf-8
import json
import os
import unittest
from dictionary.database import raw_connection
from dictionary.views import app


# Тестовые данные для заполнения БД
test_data = (
    ('foo1', 'bar1'),
    ('foo2', 'bar2'),
    ('foo3', 'bar3'),
    ('foo4', 'bar4'),
    ('foo5', 'bar5'),
)


# Путь до файла с тестовой БД
test_db_path = os.path.join(
    os.path.dirname(__file__),
    'data',
    'dict_testing.db'
)

# Путь до файла со структурой СУБД
schema_path = os.path.join(
    os.path.dirname(__file__),
    'fixtures',
    'initial_schema.sql'
)


class DictionaryTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config['DATABASE_PATH'] = test_db_path
        self.client = self.app.test_client()
        self.connection = raw_connection()

        # Заполняем тестовую СУБД
        with open(schema_path, 'r') as f:
            c = self.connection.cursor()
            c.executescript(f.read())

            for row in test_data:
                c.execute('INSERT INTO dict (key, value) VALUES (?, ?)', row)

            self.connection.commit()

    def tearDown(self):
        self.connection.close()
        os.remove(test_db_path)

    def test_get_request(self):
        with self.client as c:
            res = c.get('/dictionary/foo1')
            self.assertEqual(res.status_code, 200)
            data = json.loads(res.data)
            self.assertEqual(data['value'], 'bar1')

            self.assertEqual(c.get('/dictionary/foo6').status_code, 404)

    def test_post_request(self):
        with self.client as c:
            res = c.post(
                '/dictionary',
                data=json.dumps({'key': 'foo6', 'value': 'bar6'}))
            self.assertEqual(res.status_code, 200)
            self.assertEqual(c.get('/dictionary/foo6').status_code, 200)

            res = c.post(
                '/dictionary',
                data=json.dumps({'key': 'foo1', 'value': 'bar10'}))
            self.assertEqual(res.status_code, 409)

    def test_put_request(self):
        with self.client as c:
            res = c.put(
                '/dictionary/foo6',
                data=json.dumps({'value': 'bar6'}),
                content_type='application/json',
            )
            self.assertEqual(res.status_code, 404)

            res = c.put(
                '/dictionary/foo1',
                data=json.dumps({'value': 'bar10'}),
                content_type='application/json',
            )
            self.assertEqual(res.status_code, 200)
            res = c.get('/dictionary/foo1')
            data = self._parse_data(res.data)
            self.assertEqual('value' in data, True)
            self.assertEqual(data['value'], 'bar10')

            res = c.put(
                '/dictionary/foo1',
                content_type='application/json',
            )
            self.assertEqual(res.status_code, 400)

    def test_delete_request(self):
        with self.client as c:
            res = c.delete('/dictionary/foo1')
            self.assertEqual(res.status_code, 200)

            res = c.get('/dictionary/foo1')
            self.assertEqual(res.status_code, 404)

    def _parse_data(self, data):
        if not data:
            return {}
        return json.loads(data.decode('utf-8'))
