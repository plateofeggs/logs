# Example Logs Analysis Program

## SETTING UP THE ENVIRONMENT

This code is dependent upon the materials provided for Udacity's Logs
Analysis project. For ease of access this repository provides a vagrantfile
and two SQL scripts to set up the environment as intended for this project.  

Follow these steps to get started:

1. Download [Vagrant](https://www.vagrantup.com/) and install.
2. Download [Virtual Box](https://www.virtualbox.org/) and install. *You **do not** need to run this after installing*.
3. Clone this repository to a directory of your choice.

   Now that you have everything in place, it's time to set up your virtual environment.
   
4. `cd` into `logs` (or whatever you happened to name it):
   ```sh
   $ cd logs
   ```

5. Now let Vagrant do the hard work (this may take a few minutes to complete, be patient):
   ```sh
   $ vagrant up
   ```
   Once `vagrant up` has finished, you will be greeted with your shell prompt again.

6. Log in to the virtual machine:
   ```sh
   $ vagrant ssh
   ```
   
   If you are alerted that a restart is required above the virtual machine's prompt upon login, you can simply:
   ```sh
   $ vagrant halt
   ```
   Then
   ```sh
   $ vagrant up
   $ vagrant ssh
   ```
   
7. Once logged in, navigate to the shared directory:
   ```sh
   cd /vagrant
   ```

8. Extract the newsdata SQL script and use it to populate the database with test data:
   ```sh
   $ unzip newsdata.zip
   $ psql -d news -f newsdata.sql
   ```

9. Set up the views needed to query the database:
   ```sh
   $ psql -d news -f createviews.sql
   ```
9. Lastly, run logs.py:
   ```sh
   $ python3 logs.py
   ```

## EXPECTED OUTPUT
````

                TOP 3 ARTICLES OF ALL TIME

 "Candidate is jerk, alleges rival" -- 338647 views
 "Bears love berries, alleges bear" -- 253801 views
 "Bad things gone, say good people" -- 170098 views

                TOP AUTHORS OF ALL TIME

 Ursula La Multa -- 507594 views
 Rudolf von Treppenwitz -- 423457 views
 Anonymous Contributor -- 170098 views
 Markoff Chaney -- 84557 views

                DAYS WITH GREATER THAN 1% 404 REQUESTS

 July 17, 2016 -- 2.26 % errors
````

## VIEWS USED

This program utilizes views in PostgreSQL. The queries that make up these views are described below.

#### article_views
````sh
 SELECT count(log.path) AS views,
    log.path
   FROM log
  WHERE log.status = '200 OK'::text AND NOT log.path = '/'::text
  GROUP BY log.path
  ORDER BY (count(log.path)) DESC
 LIMIT 3;
 ````
 
 #### bad_rqst
 ````sh
 SELECT date(log."time") AS day,
   count(log.id) AS total
  FROM log
  WHERE log.status = '404 NOT FOUND'::text
  GROUP BY (date(log."time"))
  ORDER BY (date(log."time"));
````

#### good_rqst
````sh
 SELECT date(log."time") AS day,
    count(log.id) AS total
   FROM log
  GROUP BY (date(log."time"))
  ORDER BY (date(log."time"));
````

#### high_404_days
````sh
 SELECT to_char(good_rqst.day::timestamp with time zone, 'Month dd, YYYY'::text) AS to_char,
    trunc(bad_rqst.total::numeric * 100::numeric / good_rqst.total::numeric, 1) AS trunc
   FROM good_rqst
     JOIN bad_rqst ON good_rqst.day = bad_rqst.day
  WHERE (bad_rqst.total::numeric * 100::numeric / good_rqst.total::numeric) > 1::numeric;
````

#### top_articles
````sh
 SELECT articles.title,
    article_views.views
   FROM articles
     JOIN article_views ON article_views.path = ('/article/'::text || articles.slug)
  ORDER BY article_views.views DESC;
````

#### top_authors
````sh
 SELECT auth.name,
    sum(log.views) AS sum
   FROM ( SELECT authors.name,
            articles.slug
           FROM articles
             JOIN authors ON authors.id = articles.author) auth
     JOIN ( SELECT article_views.views,
            article_views.path
           FROM article_views) log ON log.path = ('/article/'::text || auth.slug)
   GROUP BY auth.name
   ORDER BY (sum(log.views)) DESC;
````

## PURPOSE OF THIS PROJECT

This project was designed to answer 3 questions about a fictional news website's traffic:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

The answers are derived from Python 3 code using the included psycopg2 library to 
connect to the website's database for analysis. 

The goal was to answer these questions in a way that utilizes only single queries to the
PostgreSQL database instead of relying on Python to do the heavy lifting. It also
displays that information in human readable format.