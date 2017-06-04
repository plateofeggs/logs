#!/bin/env/python3

#       -------------   DESCRIPTION  -------------
#   logs.py is an example of how to query a Postgresql database
#   to report data from a news website. The purpose is to obtain
#   useful information such as which authors attract the most views
#   or to find out which articles are the most popular 

import psycopg2

DBNAME = 'news'

# A function to connect to the database
def connect_to_database():
    """ Connect to the database specified in the DBNAME constant """
    database_object = psycopg2.connect(dbname=DBNAME)
    cursor = database_object.cursor()
    return cursor