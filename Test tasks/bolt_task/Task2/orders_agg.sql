/*
The following assumptions were made when completing this task:

The table should contain a set of data necessary to answer the questions in the task.
The table should not be redundant to avoid occupying additional storage space with duplicate information. In particular, fields such as "country name" and "region name" were not added to the table because they can easily be obtained using an analytical query.
This table should provide an answer to the question "how many companies were registered." Usually, this can be achieved directly using the company table. However, for the purposes of solving this task, a "left join" construction was used to answer the question within the framework of one ETL table.
*/

CREATE TABLE a
(
    admin_id INT64,
    country_code INT64,
    user_id INT64,
    order_id INT64,
    order_creation_date TIMESTAMP,
    revenue FLOAT64
);


INSERT INTO orders_agg (admin_id, country_code, user_id, order_id, order_creation_date, revenue)
WITH orders AS (
    SELECT 
        o.user_id AS user_id,
        o.order_id AS order_id,
        o.admin_id AS admin_id,
        o.created_at AS created_at,
        o.revenue AS revenue
    FROM orders AS o 
    JOIN users AS u
    ON o.user_id = u.user_id
    AND o.admin_id = u.admin_id
)
SELECT
    orders.admin_id AS admin_id,
    c.country_code AS country_code,
    user_id,
    orders.order_id AS order_id,
    orders.created_at AS order_creation_date,
    orders.revenue AS revenue
FROM company AS c 
LEFT JOIN orders;
ON c.admin_id = orders.admin_id;
