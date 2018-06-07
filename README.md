# DataSnake
CLI to query and explore different types of databases quickly and easily.

Backbone of Splunk TA-DataSnake.

## Supported Database Drivers
DataSnake should work with any database engine supported by SQLAlchemy, including:
 - PostgreSQL (through `psycopg2` or `pg8000` driver)
 - MySQL (through `mysql-connector-python`)
 - Oracle (through `cx_oracle`)
 - Microsoft SQL Server (through `pyodbc`)
 - SQLite (through `pysqlite3`)

## Usage
```
Usage:
    datasnake list-tables <connection_string>
    datasnake head-table <connection_string> <table> [--output-format=<output_format>]
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
```

`<connection_string>` is a SQLAlchemy connection string, as described [here](http://docs.sqlalchemy.org/en/latest/core/engines.html).