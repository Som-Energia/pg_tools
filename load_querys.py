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
    params = None

    def __init__(self, params):
        try:
            self.conn = psycopg2.connect(**params)
            self.params = params
        except:
            logging.error(u"I am unable to connect to the database")
        
    def getCursor(self):
        try:
            self.conn.cursor()
        except psycopg2.InterfaceError:
            self.conn = psycopg2.connect(**self.params)
        return self.conn.cursor()

    def close(self):
        self.conn.close()

    def executeStatements(self, execution, filename, outfile=None):
        cursor = self.getCursor()
        output = []
        start = timeit.default_timer()
        text_time = str(datetime.fromtimestamp(start)).decode("utf-8")
        logging.info(u"Start execute '" + execution  + u"' statemets at " + text_time)
        self.text_mail += u"Start execute '" + execution  + u"' statemets at " + text_time + u"<br>\n"
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
                    if outfile and response:
                        output.append(response)
                except psycopg2.ProgrammingError:
                    logging.error(u"Query without result: %s" % line)

        stop = timeit.default_timer()
        logging.info("uStop execute '%s' statements at %s. Execution time %s" % (execution,
            datetime.fromtimestamp(stop).strftime("%Y-%m-%d %H:%M:%S.%f").decode("utf-8"),
             str(round(stop-start,3)).decode("utf-8") + " s"))
        self.text_mail += u"Stop execute '%s' statements at %s. Execution time %s <br>\n" % (execution,
            datetime.fromtimestamp(stop).strftime("%Y-%m-%d %H:%M:%S.%f").decode("utf-8"),
             str(round(stop-start,3)).decode("utf-8") + " s")

        if outfile and output:
            outfile = outfile + str(datetime.fromtimestamp(stop)).replace(" ","_") + ".txt"
            with open(outfile, "w") as f:
                for i in output:
                    f.write(str(i))
                f.close()
        return output, outfile


    def runStatementsAndStats(self, filename, output_prefix):
        #1.- Reset postgres stats
        self.executeStatements(u"Reset stats", 'reset_stats.sql')
        #2.- Apply SQL statemetns in 'filename'
        self.executeStatements(u"SQL script of querys execution", filename)
        #3.- Force stats updated
        self.executeStatements(u"Force stats update", "analyze.sql")
        #4.- Save stats
        i = 0
        output = []
        while len(output) == 0 :
            time.sleep(10)
            output, outfilename = self.executeStatements(
                u"Save stats", u"get_stats.sql", output_prefix )
            i = i +1
            logging.info(u"Waiting for stats to be updated")
            if i == 10:
                self.executeStatements(u"Re-Force stats updated", u"analyze.sql")
                self.close()
                self.getCursor()
                i = 0

        return outfilename, output


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

    def processTuples(self, first, last):
        result = {}
        for f in first:
            print(f)
            result[f[0]] = { 'before': float(f[1]) }

        for l in last:
            if l[0] in result:
                result[l[0]]['after'] = float(l[1])
                if result[l[0]]['after'] != result[l[0]]['before']:
                    result[l[0]]['diff'] = result[l[0]]['before'] - result[l[0]]['after']
            else:
                result[l[0]] = {'after': float(l[1]) }

        return result


    def writeDiffFile(self, diff):
         with open("differences.txt", "w") as f:
            for key, value in diff.items():
                line = key.ljust(40) + ":  " + str(round(value['before'],2)).rjust(10) + " > " + str(round(value['after'],2)).rjust(10)
                if 'diff' in value:
                    line += " difference in " + str(value['diff'])
                f.write(line + "\n")

@click.command()
@click.option('--database', '-d', help=u"Existing Postgres database name")
@click.option('--dbuser', '-u', help=u"Existing Postgres user name")
@click.option('--password', '-P', help=u"Password of the user of Postgres")
@click.option('--port', '-p', default=5432, help=u"Port where Postgres is listening")
@click.option('--host', '-h', default='localhost', help=u"Server IP of Postgres")
@click.option('--filename', '-f', default='statements.sql', help=u"Filename where batch statements are")
@click.option('--filename_dba', '-a', help=u"Filename of Maintenance or DDL operations are")
def main(database, dbuser, password, port, host, filename, filename_dba):
    """Program to analyze any Maintenance or DDL operations and their impact on database performance\n
    You may want to define theses files:\n
    -  dba_modifications.sql: Maintenance or DDL operations, line by line as the example\n
    -  statements.sql: List of batch statments obtained by parse_querys.py or other tools to stress the database.
    """
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

    # Execute SQL statements and save stats
    first_stats, first_tuples = lq.runStatementsAndStats(filename, 'before_stats_')
    last_stats = None

    if filename_dba:
        # Appy DBA modificacions
        lq.executeStatements(u"Executing DBA modificacions DBA", filename_dba)
        # Retry execute SQL statements and db_stats and save it to a file
        last_stats, last_tuples = lq.runStatementsAndStats(filename, 'after_stats_')
        lq.processTuples(first_tuples, last_tuples)
        lq.writeDiffFile(first_tuples, last_tuples)
        lq.sendMail(first_stats, last_stats, 'differences.txt')

    #Send stats files by email
    lq.sendMail(first_stats)

    #Close connexion
    lq.close()

if __name__ == '__main__':
    main()

# vim: et sw=4 ts=4
