#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psycopg2
import click
import logging
from datetime import datetime
import timeit
import time
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

    def __init__(self, params):
        try:
            self.conn = psycopg2.connect(**params)
        except:
            logging.error('I am unable to connect to the database')
        
    def getCursor(self):
        return self.conn.cursor()

    def close(self):
        self.conn.close()

    def executeStatements(self, execution, filename, outfile=None):
        cursor = self.getCursor()
        output = []
        start = timeit.default_timer()
        logging.info("Start execute '%s' statemets at %s" % (execution, str(datetime.fromtimestamp(start))))
        with open(filename) as f:
            for line in f:
                cursor.execute(line)
                #TODO: Some parsing actions when we know file format
                try:
                    response = cursor.fetchall()
                    if outfile:
                        output.append(response)
                except psycopg2.ProgrammingError:
                    logging.error("Query without result: %s" % line)

        stop = timeit.default_timer()
        logging.info("Stop execute '%s' statements at %s. Execution time %s"
            % (execution, str(datetime.fromtimestamp(stop)), str(round(stop-start,3)) + " ms"))

        if outfile:
            outfile = outfile + str(datetime.fromtimestamp(stop)).strip() + ".txt"
            with open(outfile, "w") as f:
                for i in output:
                    f.write(str(i))

        return output


    def runStatementsAndStats(self, filename):
        #1.- Reinicar estadístiques de Postgres
        self.executeStatements("Reset stats", 'reset_stats.sql')
        #2.- Aplicar els statements de tot un dia extretes del pg_badger
        self.executeStatements("Executant querys", filename)
        #3.- Força l'actualització d'estadístiques
        self.executeStatements("Executat analyze", "analyze.sql")
        #4.- Extreure les estadístiques
        i = 0
        while len(self.executeStatements("Executant estadístiques", "get_stats.sql", "result_stats_")[0]) == 0:
            i = i +1
            time.sleep(10)
            logging.info("Esperant a veure si s'updaten les estadístiques")
            if i == 10:
                self.executeStatements("Executat analyze", "analyze.sql")
                i = 0

        return True


@click.command()
@click.option('--database', '-d')
@click.option('--dbuser', '-u')
@click.option('--password', '-P')
@click.option('--port', '-p', default=5432)
@click.option('--host', '-h', default='localhost')
@click.option('--filename', '-f', default='statements20200429.sql')
@click.option('--filename_dba', '-a')
def main(database, dbuser, password, port, host, filename, filename_dba):
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
    lq.runStatementsAndStats(filename)

    if filename_dba:
        # Apliquem les modificacions
        lq.executeStatements("Executant modificacions DBA", filename_dba)
        # Tornem a fer el proces
        lq.runStatementsAndStats(filename)

    #Pugem els fitxers de stats algun lloc


    #Tancar connexió
    lq.close()

if __name__ == '__main__':
    main()

# vim: et sw=4 ts=4
