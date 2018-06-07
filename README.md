# DataSnake
CLI to query and explore different types of databases quickly and easily.

Backbone of Splunk TA-DataSnake.

## Usage
```
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
```