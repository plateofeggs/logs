#!/bin/env/python3

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
    return cursor.fetchall()
    database_object.close()

def top_three_articles_alltime():
    """ Print the three most popular articles of all time """
    top_three = process_query(("select count(path), articles.slug "
                               "from log join articles "
                               "on log.path = '/article/' || articles.slug "
                               "group by articles.slug "
                               "order by count(path) desc limit 3"))
    rank = 1
    print("\n\t\tTOP 3 ARTICLES\n")
    print("Rank \t|\tViews \t|\tArticle Name")
    print("-------------------------------------------------------")

    for article in top_three:
        print(str(rank) + "\t\t" + str(article[0]) + "\t\t" + article[1])
        rank += 1


# Who are the most popular article authors of all time?
def top_authors_alltime():
    pass

# On which days did more than 1% of requests lead to errors?
def error_prone_days():
    pass

top_three_articles_alltime()