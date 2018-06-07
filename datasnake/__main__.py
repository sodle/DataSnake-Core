#!/usr/bin/env python
"""Query and explore different types of databases quickly and easily.

Usage:
    datasnake list-tables <connection_string> [--output-format=<output_format>]
    datasnake head-table <connection_string> <table>
    datasnake <connection_string> <sql_query> [--output-format=<output_format>]
    datasnake <connection_string> <sql_query> --index=<index> [--offset=<offset>] [--output-format=<output_format>]
    datasnake (-h | --help)
    datasnake --version

Options:
    -h --help                           Show this help.
    --version                           Show version.
    --index=<index>                     Column to use as index (for sorting and checkpointing).
    --offset=<offset>                   Only fetch rows with index value strictly greater than this.
    --output-format=<output_format>     Output rows in "dbx" (Splunk DBX) or "json" format [default: dbx].
"""
from __future__ import print_function
import sys
import json
from time import time
from docopt import docopt
from six import iteritems
from sqlalchemy import create_engine
from pandas import read_sql_query, read_sql_table, DataFrame


def print_error(msg):
    print('ERROR\t{}'.format(msg), file=sys.stderr)


def print_warning(msg):
    print('WARN\t{}'.format(msg), file=sys.stderr)


def print_info(msg):
    print('INFO\t{}'.format(msg), file=sys.stderr)


def print_debug(msg):
    print('DEBUG\t{}'.format(msg), file=sys.stderr)


def print_row(timestamp, row):
    print('ROW\t{}\t{}'.format(timestamp, row))


def print_table(table):
    print('TABLE\t{}'.format(table))


def print_checkpoint(timestamp):
    print('CHECKPOINT\t{}'.format(timestamp))


formatters = {
    'dbx': lambda row: ' '.join(['{}={}'.format(k, v) for k, v in iteritems(row)]),
    'json': lambda row: json.dumps({k: v for k, v in iteritems(row)})
}


def list_tables(connection_string):
    engine = create_engine(connection_string)
    tables = engine.table_names()
    print_info('Found {} tables'.format(len(tables)))
    if len(tables) == 0:
        print_warning('No tables found')
    for table in tables:
        print_table(table)


def run_query(connection_string, sql_query, index=None, offset=None, output_format='dbx'):
    try:
        formatter = formatters[output_format]
    except KeyError:
        print_error('Invalid output format "{}" - try "dbx" or "json"'.format(output_format))
        return
    engine = create_engine(connection_string)
    df = read_sql_query(sql_query, engine, index_col=index)
    if index is not None and offset is not None:
        df = df[df.index > float(offset)]
    for idx, row in df.iterrows():
        timestamp = idx if index is not None else time()
        print_row(timestamp, formatter(row))
    if index is not None:
        print_checkpoint(df.index.max())


def head_table(connection_string, table, output_format='dbx'):
    try:
        formatter = formatters[output_format]
    except KeyError:
        print_error('Invalid output format "{}" - try "dbx" or "json"'.format(output_format))
        return
    engine = create_engine(connection_string)
    df = read_sql_table(table, engine)
    for idx, row in DataFrame(df.head()).iterrows():
        timestamp = time()
        print_row(timestamp, formatter(row))


def _main():
    arguments = docopt(__doc__, version='datasnake 0.1.0')

    if arguments['list-tables']:
        list_tables(arguments['<connection_string>'])
    elif arguments['head-table']:
        head_table(arguments['<connection_string>'], arguments['<table>'], output_format=arguments['--output-format'])
    else:
        run_query(arguments['<connection_string>'], arguments['<sql_query>'], index=arguments['--index'],
                  offset=arguments['--offset'], output_format=arguments['--output-format'])


if __name__ == '__main__':
    _main()
