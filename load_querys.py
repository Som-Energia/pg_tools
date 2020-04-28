#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psycopg2
import click
import logging
import datetime
import timeit

"""
Proposem:
1.- Crear una màquina amb Snapshot de SP1 i li direm TSP1 (sysadmin)
2.- Fer un Savepoint a TSP1 (sysadmin)
3.- Reiniciar estadístiques (script nostre)
4.- Aplicar totes les querys d'un dia extretes del pg_badger (script nostre)
5.- Guardem i reiniciem les estadístiques (script nostre)
6.- Tornar a Savepoint a TSP1 (sysadmin)
7.- Aplicar les millores que vulguem provar (REINDEX, CLUSTER…) (dba actions)
8.- Tornar a aplicar les querys d’un dia extretes del pg_badger (script nostre)
9.- Comparar estadístiques actuals amb les guardades (dba actions)

Script (o manual de moment):
1.- Reinicar estadístiques de Postgres
2.- Aplicar els statements de tot un dia extretes del pg_badger
3.- Extreure les estadístiques i enviar-es/guardels fora

Un altre script (o manualment de moment)
4.- Que compari estadístiques


Mode d'execució:
python load_querys.py -d NOM_BASEDADES -u USUARI -P PASSWORD [ -h SERVIDOR ] [-p PORT]
p. ex: python load_querys.py -d somenergia -u user -P password -h localhost
"""
class LoadQuerys(object):
    conn = None
    logger = None

    def __init__(self, params):
        self.logger = logging.getLogger('LoadQuerys')

        try:
            self.conn = psycopg2.connect(**params)
        except:
            self.logger.error('I am unable to connect to the database')
        
    def getCursor(self):
        return self.conn.cursor()

    def resetStats(self):
        cursor = self.getCursor()
        cursor.execute("select pg_stat_reset();")
        self.logger.info("The stats has been reseted")

    def executeStatements(self, filename):
        cursor = self.getCursor()
        start = timeit.default_timer()
        self.logger.info("Start execute statemets at %s" % str(start))
        with open(filename) as f:
           for line in f:
                #TODO: Some parsing actions when we know file format
               cursor.execute(f)
        stop = timeit.default_timer()
        self.logger.info("Start execute statements at %s. Execution time %s"
            % (str(stop), str(stop-start)))

        return True

@click.command()
@click.option('--database', '-d')
@click.option('--dbuser', '-u')
@click.option('--password', '-P')
@click.option('--port', '-p')
@click.option('--host', '-h', default='localhost')
@click.option('--filename', '-f', default='statements20200429.sql')
def main(database, dbuser, password, port, host, filename):
    config = {
        'host': host,
        'database': database,
        'user': dbuser,
        'password': password,
        'port': port
    }
    lq = LoadQuerys(config)
    lq.getCursor() 
    #1.- Reinicar estadístiques de Postgres
    lq.resetStats()
    #2.- Aplicar els statements de tot un dia extretes del pg_badger
    lq.executeStatements(filename)
    #3.- Extreure les estadístiques i enviar-es/guardels fora


if __name__ == '__main__':
    main()

# vim: et sw=4 ts=4
