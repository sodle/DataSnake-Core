#!/usr/bin/env python
"""Query and explore different types of databases quickly and easily.

Usage:
    datasnake <connection_string> <sql_query> [--output-format=<output_format>]
    datasnake <connection_string> <sql_query> --index=<index> [--offset=<offset>] [--output-format=<output_format>]
    datasnake list-tables <connection_string>
    datasnake (-h | --help)
    datasnake --version

Options:
    -h --help                           Show this help.
    --version                           Show version.
    --index=<index>                     Column to use as index (for sorting and checkpointing).
    --offset=<offset>                   Only fetch rows with index value strictly greater than this.
    --output-format=<output_format>     Output rows in "dbx" (Splunk DBX) or "json" format [default: dbx].
"""
from docopt import docopt


def list_tables(connection_string):
    pass


def run_query(connection_string, sql_query, index=None, offset=0, output_format='dbx'):
    pass


def _main():
    arguments = docopt(__doc__, version='datasnake 0.1.0')

    if arguments['list-tables']:
        list_tables(arguments['connection_string'])
    else:
        run_query(arguments['connection_string'], arguments['sql_query'], index=arguments['index'],
                  offset=arguments['offset'], output_format=arguments['output_format'])


if __name__ == '__main__':
    _main()
