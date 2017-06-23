CREATE VIEW article_views AS 
 SELECT count(log.path) AS views,
    log.path
   FROM log
  WHERE log.status = '200 OK'::text AND NOT log.path = '/'::text
  GROUP BY log.path
  ORDER BY (count(log.path)) DESC
 LIMIT 3;
 
 CREATE VIEW bad_rqst AS 
SELECT date(log.time) AS day,
  count(log.id) AS total
 FROM log
 WHERE log.status = '404 NOT FOUND'::text
 GROUP BY (date(log.time))
 ORDER BY (date(log.time));
 
 CREATE VIEW good_rqst AS 
 SELECT date(log.time) AS day,
    count(log.id) AS total
   FROM log
  GROUP BY (date(log.time))
  ORDER BY (date(log.time));
 
 CREATE VIEW high_404_days AS
 SELECT good_rqst.day AS day,
    bad_rqst.total::numeric * 100::numeric / good_rqst.total::numeric AS percentage
   FROM good_rqst
     JOIN bad_rqst ON good_rqst.day = bad_rqst.day
  WHERE (bad_rqst.total::numeric * 100::numeric / good_rqst.total::numeric) > 1::numeric;
