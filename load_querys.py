# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import psycopg2
import click
import logging
from datetime import datetime
import timeit
import time
import emili

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

Per parsejar el log de postgres, fer servir el parse_querys.py
python parse_querys.py -l postgresql-2020-04-23_000000.log
"""

class LoadQuerys(object):
    conn = None
    text_mail = u""

    def __init__(self, params):
        try:
            self.conn = psycopg2.connect(**params)
            self.conn.cursor()
        except:
            logging.error('I am unable to connect to the database')
        
    def getCursor(self):
        return self.conn.cursor()

    def close(self):
        self.conn.close()

    def executeStatements(self, execution, filename, outfile=None):
        #if not outfile:
        #    return True
        cursor = self.getCursor()
        output = []
        start = timeit.default_timer()
        text_time = str(datetime.fromtimestamp(start)).decode("utf-8")
        logging.info("Start execute " + execution  + " statemets at " + text_time)
        self.text_mail += "Start execute " + execution  + " statemets at " + text_time + "<br>\n"
        with open(filename) as f:
            for line in f:
                # Skip comment lines
                print(line)
                if line.startswith("--"):
                    continue
                cursor.execute(line)
                #TODO: Some parsing actions when we know file format
                try:
                    response = cursor.fetchall()
                    if outfile:
                        output.append(response)
                except psycopg2.ProgrammingError:
                    logging.error("Query without result: %s" % line)

        stop = timeit.default_timer()
        logging.info("Stop execute '%s' statements at %s. Execution time %s" % (execution,
            datetime.fromtimestamp(stop).strftime("%Y-%m-%d %H:%M:%S.%f").decode("utf-8"),
             str(round(stop-start,3)).decode("utf-8") + " s"))
        self.text_mail += u"Stop execute '%s' statements at %s. Execution time %s <br>\n" % (execution,
            datetime.fromtimestamp(stop).strftime("%Y-%m-%d %H:%M:%S.%f").decode("utf-8"),
             str(round(stop-start,3)).decode("utf-8") + " s")

        if outfile:
            outfile = outfile + str(datetime.fromtimestamp(stop)).replace(" ","_") + ".txt"
            with open(outfile, "w") as f:
                for i in output:
                    f.write(str(i))
                f.close()
        return output, outfile


    def runStatementsAndStats(self, filename, output_prefix):
        #1.- Reinicar estadístiques de Postgres
        self.executeStatements("Reset stats", 'reset_stats.sql')
        #2.- Aplicar els statements de tot un dia extretes del pg_badger
        self.executeStatements("Executant querys", filename)
        #3.- Força l'actualització d'estadístiques
        self.executeStatements("Executat analyze", "analyze.sql")
        #4.- Extreure les estadístiques
        i = 0
        output = []
        while len(output) == 0 :
            output, outfilename = self.executeStatements(
                "Executant estadístiques", "get_stats.sql", output_prefix )
            i = i +1
            time.sleep(10)
            logging.info("Esperant a veure si s'updaten les estadístiques")
            if i == 10:
                self.executeStatements("Executat analyze", "analyze.sql")
                i = 0

        return outfilename


    def sendMail(self, first_stats, last_stats):
        attachments = [first_stats]
        if last_stats:
            attachments.append(last_stats)
        body = u"This is the result of your recent execution. Feel free to decide to apply the same recipes in production ;) <br>\n"
        body += self.text_mail
        emili.sendMail(
            sender = 'sistemes@somenergia.coop',
            to = ['oriol.piera@somenergia.coop'],
            subject = u"pg_tools: Postgres Stats",
            md = body,
            attachments = attachments,
            config = '../dbconfig.py',
        )


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
    dbconfig = {
        'host': host,
        'database': database,
        'user': dbuser,
        'password': password,
        'port': port
    }
    lq = LoadQuerys(dbconfig)
    lq.getCursor()

    # Executem sql simulació càrrega i guardem stats
    first_stats = lq.runStatementsAndStats(filename, 'before_stats_')
    last_stats = None

    if filename_dba:
        # Apliquem les modificacions
        lq.executeStatements("Executant modificacions DBA", filename_dba)
        # Tornem a fer el proces
        last_stats = lq.runStatementsAndStats(filename, 'after_stats_')

    #Pugem els fitxers de stats algun lloc
    lq.sendMail(first_stats, last_stats)

    #Tancar connexió
    lq.close()

if __name__ == '__main__':
    main()

# vim: et sw=4 ts=4
