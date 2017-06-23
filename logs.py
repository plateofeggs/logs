#!/usr/bin/env python3
#       -------------   DESCRIPTION  -------------
#   logs.py is an example of how to query a Postgresql database
#   to report data from a news website. The purpose is to obtain
#   useful information such as which authors attract the most views
#   or to find out which articles are the most popular

import psycopg2

DBNAME = 'news'


def process_query(user_query):
    """ Return the result of a given query """
    database_object = psycopg2.connect(dbname=DBNAME)
    cursor = database_object.cursor()
    cursor.execute(user_query)
    results = cursor.fetchall()
    database_object.close()
    return results


def top_three_articles_alltime():
    """ Print the three most popular articles of all time """
    top_three = process_query(("select * from top_three_articles"))

    print("\n    \t    \t    TOP 3 ARTICLES\n    ")

    for title, views in top_three:
        print("\"{}\" -- {} views".format(title, views))


def top_authors_alltime():
    """ Print the top authors of all time """
    top_authors = process_query(("select * from top_authors"))
    print("\n    \t    \t    TOP AUTHORS\n    ")

    for name, views in top_authors:
        print("{} -- {} views".format(name, views))


def error_prone_days():
    """ Print the days in which there were more than 1% bad requests """
    high_404_days = process_query("select * from high_404_days")

    print("\n    \t    \t    DAYS WITH GREATER THAN 1% 404 REQUESTS\n    ")

    for day, percentage in high_404_days:
        print(" {0:%B %d, %Y} -- {1:.2f} % errors".format(day, percentage))


if __name__ == '__main__':
    top_three_articles_alltime()
    top_authors_alltime()
    error_prone_days()
