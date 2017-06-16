#! /usr/bin/env/python3
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
    top_three = process_query(("select title, article_views.views "
                               "from articles join article_views "
                               "on article_views.path = '/article/' "
                               "|| articles.slug "
                               "order by article_views.views desc"))

    print("\n    \t    \t    TOP 3 ARTICLES\n    ")

    for article in top_three:
        print(article[0] + "\t    -\t    " + str(article[1]))


# Who are the most popular article authors of all time?
def top_authors_alltime():
    top_authors = process_query(("select auth.name, sum(log.views) "
                                 "from (select authors.name, articles.slug "
                                 "from articles join authors "
                                 "on authors.id = articles.author) auth "
                                 "join "
                                 "(select count(log.path) as views, "
                                 "log.path "
                                 "from log where status = '200 OK' "
                                 "and not path = '/' "
                                 "group by path) log "
                                 "on log.path = '/article/' || auth.slug "
                                 "group by auth.name "
                                 "order by sum(log.views) desc"))

    print("\n    \t    \t    TOP AUTHORS\n    ")

    for author in top_authors:
        print(author[0] + "\t    -\t    " + str(author[1]))


# On which days did more than 1% of requests lead to errors?
def error_prone_days():
    high_404_days = process_query("select * from high_404_days")

    print("\n    \t    \t    DAYS WITH GREATER THAN 1% 404 REQUESTS\n    ")

    for day in high_404_days:
        print(day[0] + "\t    -\t    " + str(day[1]))


top_three_articles_alltime()
top_authors_alltime()
error_prone_days()
