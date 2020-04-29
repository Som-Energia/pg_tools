#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psycopg2
import click
import logging
from datetime import datetime
import timeit
import time
import postgresql_log_parser
from postgresql_log_parser.parsers import PyParsingParser, RegexpParser
from postgresql_log_parser.repositories import InMemoryRepository
from postgresql_log_parser.services import LogParserService

class LoadQuerys(object):
    conn = None

    def __init__(self, params):
        try:
            self.conn = psycopg2.connect(**params)
        except:
            logging.error('I am unable to connect to the database')
        
    def getCursor(self):
        return self.conn.cursor()

    def close(self):
        self.conn.close()

    def parseQuerys(self, filename):
        import pudb;pu.db
        parser_pyparsing = RegexpParser()
        repository = InMemoryRepository()
        service_pyparsing = LogParserService(repository, parser=parser_pyparsing)
        service_pyparsing.parse_file(filename)
        parsed_data = repository.get_all()
        print(parsed_data)
        #https://regex101.com/
        regex = "((?P<new_entrance>((?P<date>\d{4}-\d{2}-\d{2}\s\d{2}\:\d{2}\:\d{2}\.\d{3})\s(?P<host>[a-zA-Z0-9-]{4})\s(?P<pid>\[\d+\])\suser=(?P<user>[a-z0-9-_\[\]]+),host=(?P<ip>[0-9.]+),db=(?P<database>[a-z0-9-_\]\[]+),session=(?P<session>[a-zA-Z0-9-.\/]+)\s)STATEMENT:(?P<query>.+))|(?P<new_entrance2>((?P<date2>\d{4}-\d{2}-\d{2}\s\d{2}\:\d{2}\:\d{2}\.\d{3})\s(?P<host2>[a-zA-Z0-9-]{4})\s(?P<pid2>\[\d+\])\suser=(?P<user2>[a-z0-9-_\[\]]+),host=(?P<ip2>[0-9.]+),db=(?P<database2>[a-z0-9-_\]\[]+),session=(?P<session2>[a-zA-Z0-9-.\/]+)\s))|.*)"
        #print(parsed_data['query'])


@click.command()
@click.option('--database', '-d')
@click.option('--dbuser', '-u')
@click.option('--password', '-P')
@click.option('--port', '-p', default=5432)
@click.option('--host', '-h', default='localhost')
@click.option('--filename', '-f', default='statements20200429.sql')
@click.option('--postgres_log', '-l', default='postgresql.log')
@click.option('--filename_dba', '-a')
def main(database, dbuser, password, port, host, filename, filename_dba, postgres_log):
    logging.basicConfig(filename='loadquerys.log', level=logging.INFO)
    config = {
        'host': host,
        'database': database,
        'user': dbuser,
        'password': password,
        'port': port
    }
    lq = LoadQuerys(config)
    lq.getCursor()
    #pg_stats_statements
    # Executem sql simulació càrrega i guardem stats
    lq.parseQuerys(postgres_log)
    #Tancar connexió
    lq.close()

if __name__ == '__main__':
    main()

# vim: et sw=4 ts=4
