#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
import logging
from datetime import datetime
import timeit
import time
import re
"""
Tool to parser the Postgres log and write a SQL script with all STATEMENTS (SELECTS, UPDATES, INSERTS and DELETES)
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
        logging.info(u"Match query: '" + str(output))
    file_times.close()


@click.command()
@click.option('--postgres_log', '-l', default='postgresql.log', help='Postgres log file')
def main(postgres_log):
    """Simple program that parse Postgres log file and creates SQL script with Statements\n
    Log format:\n
    2020-04-23 13:11:44.057 CEST [18319] user=,host=,db=,session=5ea177ef.478f 124/122307 STATEMENT:  select account_invoice.id from "account_invoice" order by id desc
    """
    logging.basicConfig(filename='parsequerys.log', level=logging.INFO)
    parseQuerys(postgres_log)


if __name__ == '__main__':
    main()

# vim: et sw=4 ts=4
