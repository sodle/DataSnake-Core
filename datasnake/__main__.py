#!/usr/bin/env python
"""Query and explore different types of databases quickly and easily.

Usage:
    datasnake list-tables <connection_string>
    datasnake head-table <connection_string> <table> [--output-format=<output_format>]
    datasnake <connection_string> <sql_query> [--output-format=<output_format>]
    datasnake <connection_string> <sql_query> --index=<index> [--offset=<offset>] [--output-format=<output_format>]
    datasnake (-h | --help)
    datasnake --version
    datasnake --env

Options:
    -h --help                           Show this help.
    --version                           Show version.
    --env                               Show installed DataSnake and database connector versions as JSON.
    --index=<index>                     Column to use as index (for sorting and checkpointing).
    --offset=<offset>                   Only fetch rows with index value strictly greater than this.
    --output-format=<output_format>     Output rows in "dbx" (Splunk DBX) or "json" format [default: dbx].
"""
from __future__ import print_function
import sys
import json
from docopt import docopt
from six import iteritems
from sqlalchemy import create_engine
from pandas import read_sql_query, read_sql_table, to_numeric, Series


__version__ = '0.2.4'


def print_error(msg):
    print('ERROR\t{}'.format(msg), file=sys.stderr)


def print_warning(msg):
    print('WARN\t{}'.format(msg), file=sys.stderr)


def print_info(msg):
    print('INFO\t{}'.format(msg), file=sys.stderr)


def print_debug(msg):
    print('DEBUG\t{}'.format(msg), file=sys.stderr)


def print_row(timestamp, row):
    print(timestamp)
    print('ROW\t{}\t{}'.format(timestamp, row))


def print_table(table):
    print('TABLE\t{}'.format(table))


def print_checkpoint(timestamp):
    print('CHECKPOINT\t{}'.format(timestamp))


def format_dbx(row):
    return ' '.join(['{}={}'.format(k, v) for k, v in iteritems(row)])


def list_tables(connection_string):
    engine = create_engine(connection_string)
    tables = engine.table_names()
    print_info('Found {} tables'.format(len(tables)))
    if len(tables) == 0:
        print_warning('No tables found')
    for table in tables:
        print_table(table)


def run_query(connection_string, sql_query, index=None, offset=None, output_format='dbx'):
    if output_format not in ['dbx', 'json']:
        print_error('Invalid output format "{}" - try "dbx" or "json"'.format(output_format))
        return
    engine = create_engine(connection_string)
    df = read_sql_query(sql_query, engine, parse_dates=[index] if index is not None else [])
    if index is not None:
        df['__ds_checkpoint'] = to_numeric(df[index])
        df = df.set_index('__ds_checkpoint')
    if index is not None and offset is not None:
        df = df[df.index > float(offset)]
    if output_format == 'json':
        fmt = df.to_json(orient='records', lines=True).split('\n')
        out = Series(fmt, index=df.index)
    else:
        out = df.apply(format_dbx, axis=1)
    for idx, row in out.iteritems():
        print_row(idx, row)
    if index is not None and df.shape[0] > 0:
        print_checkpoint(df.index.max())


def head_table(connection_string, table, output_format='dbx'):
    if output_format not in ['dbx', 'json']:
        print_error('Invalid output format "{}" - try "dbx" or "json"'.format(output_format))
        return
    engine = create_engine(connection_string)
    df = read_sql_table(table, engine)
    if output_format == 'json':
        fmt = df.to_json(orient='records', lines=True).split('\n')
    else:
        fmt = df.apply(format_dbx, axis=1)
    out = Series(fmt, index=df.index)
    for idx, row in out.iteritems():
        print_row(idx, row)


def print_env():
    py_version = '{}.{}.{}'.format(*sys.version_info[:3])
    version = {
        'Python': '{} ({})'.format(py_version, sys.executable),
        'DataSnake Core': __version__
    }
    try:
        import psycopg2
        version['PostgreSQL - psycopg2'] = psycopg2.__version__
    except ImportError:
        version['PostgreSQL - psycopg2'] = 'Not installed'
    try:
        import pg8000
        version['PostgreSQL - pg8000'] = pg8000.__version__
    except ImportError:
        version['PostgreSQL - pg8000'] = 'Not installed'
    try:
        import mysql.connector
        version['MySQL - mysql-connector-python'] = mysql.connector.__version__
    except ImportError:
        version['MySQL - mysql-connector-python'] = 'Not installed'
    try:
        import cx_Oracle
        version['Oracle - cx_Oracle'] = cx_Oracle.__version__
    except ImportError:
        version['Oracle - cx_Oracle'] = 'Not installed'
    try:
        import pyodbc
        version['MSSQL/Sybase - pyodbc'] = pyodbc.version
    except ImportError:
        version['MSSQL/Sybase - pyodbc'] = 'Not installed'
    try:
        import sqlite3
        version['SQLite - Native Python driver'] = 'Available'
    except ImportError:
        version['SQLite - Native Python driver'] = 'Not available - Python was not installed with SQLite support'
    print(json.dumps(version))


def _main():
    arguments = docopt(__doc__, version='datasnake {}'.format(__version__))

    if arguments['--env']:
        print_env()
        return

    if arguments['list-tables']:
        list_tables(arguments['<connection_string>'])
    elif arguments['head-table']:
        head_table(arguments['<connection_string>'], arguments['<table>'], output_format=arguments['--output-format'])
    else:
        run_query(arguments['<connection_string>'], arguments['<sql_query>'], index=arguments['--index'],
                  offset=arguments['--offset'], output_format=arguments['--output-format'])


if __name__ == '__main__':
    _main()
