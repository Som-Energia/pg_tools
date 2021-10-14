# pg_tools
PostgreSQL tools

## parse_querys.py
Read the Postgres log file and extract all the Statements (SELECT, INSERT, UPDATE and DELETE) to an SQL script ready to load to an existing database.

### Comand line usage
```
Usage: parse_querys.py [OPTIONS]

  Simple program that parse Postgres log file and creates SQL script with
  Statements

  Log format:

  2020-04-23 13:11:44.057 CEST [18319] user=,host=,db=,session=5ea177ef.478f
  124/122307 STATEMENT:  select account_invoice.id from "account_invoice"
  order by id desc

Options:
  -l, --postgres_log TEXT  Postgres log file
  --help                   Show this message and exit.
```

## load_querys.py
This program make this operations in a row:
1.- Reset database stats
1.- Execute operations in statements.sql or file passed by '-f' option
1.- Save database stats in before_stats_TIMESTAMP.txt file and reset database stats
1.- Execute Maintenance or DDL operations in dba_modifications.sql or file passed by '-a' option
1.- Execute operations in statements.sql or file passed by '-f' option
1.- Save database stats in after_stats_TIMESTAMP.txt file and reset database stats
1.- Send it by email

### Comand line usage
```
Usage: load_querys.py [OPTIONS]

  Program to analyze any Maintenance or DDL operations and their impact on
  database performance

  You may want to define theses files:

  -  dba_modifications.sql: Maintenance or DDL operations, line by line as
  the example

  -  statements.sql: List of batch statments obtained by parse_querys.py or
  other tools to stress the database.

Options:
  -d, --database TEXT      Existing Postgres database name
  -u, --dbuser TEXT        Existing Postgres user name
  -P, --password TEXT      Password of the user of Postgres
  -p, --port INTEGER       Port where Postgres is listening
  -h, --host TEXT          Server IP of Postgres
  -f, --filename TEXT      Filename where batch statements are
  -a, --filename_dba TEXT  Filename of Maintenance or DDL operations are
  --help                   Show this message and exit.
```

