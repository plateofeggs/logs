# Example Logs Analysis Program

## SETTING UP THE ENVIRONMENT

This project is dependent upon the materials provided for Udacity's Logs
Analysis project. 

1. Instructions for setting up this environment can be located [here](https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0)

2. Additionally, you will need to download the PostgreSQL database [here](https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/262a84d7-86dc-487d-98f9-648aa7ca5a0f/concepts/a9cf98c8-0325-4c68-b972-58d5957f1a91)
and follow the subsequent instructions

3. Clone this project into the shared /vagrant directory and cd in to it

4. If you have not already:
```sh
$ vagrant up
$ vagrant ssh
````

5. From the virtual machine prompt (substitue '/logs' with your custom directory name if needed):
````sh
$ cd /vagrant/logs
````

## CREATING THE VIEWS

This program utilizes views in PostgreSQL. To set these up, do the following:

````sh
/vagrant/logs$ psql -d news

news=> CREATE VIEW article_views AS 
 SELECT count(log.path) AS views,
    log.path
   FROM log
  WHERE log.status = '200 OK'::text AND NOT log.path = '/'::text
  GROUP BY log.path
  ORDER BY (count(log.path)) DESC
 LIMIT 3;
 ````
 ````sh
news=> CREATE VIEW bad_rqst AS 
 SELECT date(log."time") AS day,
   count(log.id) AS total
  FROM log
  WHERE log.status = '404 NOT FOUND'::text
  GROUP BY (date(log."time"))
  ORDER BY (date(log."time"));
````
````sh
news=> CREATE VIEW good_rqst AS 
 SELECT date(log."time") AS day,
    count(log.id) AS total
   FROM log
  GROUP BY (date(log."time"))
  ORDER BY (date(log."time"));
````
````sh
news=> CREATE VIEW high_404_days AS
 SELECT to_char(good_rqst.day::timestamp with time zone, 'Month dd, YYYY'::text) AS to_char,
    trunc(bad_rqst.total::numeric * 100::numeric / good_rqst.total::numeric, 1) AS trunc
   FROM good_rqst
     JOIN bad_rqst ON good_rqst.day = bad_rqst.day
  WHERE (bad_rqst.total::numeric * 100::numeric / good_rqst.total::numeric) > 1::numeric;
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
displays that information in human readable format