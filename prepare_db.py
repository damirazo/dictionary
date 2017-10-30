# coding: utf-8
import os
import sqlite3


def init_db():
    project_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'src',
        'dictionary')
    path = os.path.join(
        project_path,
        'fixtures',
        'initial_schema.sql')

    with open(path, 'r') as f:
        db = sqlite3.connect(os.path.join(project_path, 'data', 'dict.db'))
        db.cursor().executescript(f.read())
        db.commit()


if __name__ == '__main__':
    init_db()
