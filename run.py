# coding: utf-8
import sys
import os


sys.path.insert(
    0, os.path.join(os.path.abspath(os.path.dirname(__file__)), 'src'))


if __name__ == '__main__':
    from dictionary.views import app

    app.config['DATABASE_PATH'] = os.path.join(
        os.path.dirname(__file__),
        'src', 'dictionary', 'data', 'dict.db'
    )
    app.run()
