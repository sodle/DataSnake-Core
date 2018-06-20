#!/usr/bin/env python
from setuptools import setup

setup(
    name='datasnake',
    version='0.2.3',
    description='CLI for fast and easy database queries, tailing, pagination, introspection. '
                'DB engine agnostic. Backbone of Splunk TA-DataSnake.',
    author='Scott Odle (Arizona State University)',
    author_email='scott.odle@asu.edu',
    url='https://github.com/sodle/datasnake-core',
    license=['GPL v3'],
    packages=['datasnake'],
    install_requires=[
        'six',
        'pandas',
        'sqlalchemy',
        'docopt',
        'psycopg2-binary',
        'pg8000',
        'mysql-connector-python',
        'cx_oracle',
        'pyodbc',
        'pysqlite3'
    ],
    entry_points={
        'console_scripts': [
            'datasnake = datasnake.__main__:_main'
        ]
    }
)
