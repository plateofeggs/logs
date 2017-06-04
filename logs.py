#!/bin/env/python3

#       -------------   DESCRIPTION  -------------
#   logs.py is an example of how to query a Postgresql database
#   to report data from a news website. The purpose is to obtain
#   useful information such as which authors attract the most views
#   or to find out which articles are the most popular 

import psycopg2

DBNAME = 'news'

def process_query(user_query):
    """ Take a query as input and return the result of that query """
    database_object = psycopg2.connect(dbname=DBNAME)
    cursor = database_object.cursor()
    cursor.execute(user_query)
    return cursor.fetchall()
    database_object.close()