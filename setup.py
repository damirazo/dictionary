# coding:utf-8
from pip.download import PipSession
from pip.req import parse_requirements
from setuptools import setup, find_packages


setup(
    name='dictionary',
    version='0.1',
    author='damirazo',
    author_email='me@damirazo.ru',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    description=open('README').read(),
    install_requires=parse_requirements(
        'requirements.txt',
        session=PipSession(),
    ),
)
