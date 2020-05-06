#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
import logging
from datetime import datetime
import timeit
import time
import re
"""
Eina per parsejar el log de Postgres i extreure els STATEMENTS (SELECTS, UPDATES, INSERTS, DELETES...)
python parse_querys.py -l postgresql-2020-04-23_000000.log
"""

def parseQuerys(filename):
    regex = r"(?P<metadata>.*)STATEMENT:  (?P<query>[\w\n\s\(\)\.,'\"\*\-+=<>:\/]*([;']|$)[\w\n\s\(\)\.,'\"\*\-+=<>:\/]*$|[^;]*)"
    ifile = open(filename,'r')
    test_str = ifile.read()
    ifile.close()

    matches = re.finditer(regex, test_str, re.MULTILINE)
    file_times = open(filename + "_parsed_querys.sql","w")
    for matchNum, match in enumerate(matches, start=1):
        output = match.group("query") + ";\n"
        file_times.write(output)
    file_times.close()


@click.command()
@click.option('--postgres_log', '-l', default='postgresql.log')
def main(postgres_log):
    # Executem sql simulació càrrega i guardem stats
    parseQuerys(postgres_log)


if __name__ == '__main__':
    main()

# vim: et sw=4 ts=4
