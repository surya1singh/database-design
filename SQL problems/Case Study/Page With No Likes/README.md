# [Page With No Likes](https://github.com/surya1singh/database-design/blob/main/SQL%20problems/Case%20Study/Page%20With%20No%20Likes/Page%20with%20No%20Likes.ipynb) this problem is taken from [here](https://datalemur.com/questions/sql-page-with-no-likes)
Compare Except operator, join, Not In and Not Exists

# SQL Query Benchmarking on PostgreSQL RDS

## Overview
This project benchmarks different SQL queries to identify the most efficient way to find `page_id`s that exist in the `pages` table but not in the `page_likes` table. The tests were conducted on **Amazon RDS PostgreSQL** using a `db.m5.xlarge` instance with **4 vCPUs and 16GB RAM**.

## Database Schema
```sql
CREATE TABLE IF NOT EXISTS pages (
    page_id INT NOT NULL PRIMARY KEY,
    page_name VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS page_likes (
    user_id INT NOT NULL,
    page_id INT NOT NULL
);

CREATE INDEX page_likes_page_id ON page_likes (page_id);
```

Both tables contain **500,000,000** records.

## Queries Tested

### 1. Using `EXCEPT`
```sql
SELECT COUNT(*) FROM (
    SELECT page_id
    FROM pages
    EXCEPT
    SELECT page_id
    FROM page_likes
) AS subquery;
```
**Execution Time:** ~14 minutes 12 seconds

### 2. Using `LEFT JOIN ... WHERE IS NULL`
```sql
SELECT COUNT(*) FROM (
    SELECT pages.page_id
    FROM pages
    LEFT JOIN page_likes ON pages.page_id = page_likes.page_id
    WHERE page_likes.page_id IS NULL
) AS subquery;
```
**Execution Time:** ~3 minutes 44 seconds

### 3. Using `NOT EXISTS`
```sql
SELECT COUNT(*) FROM (
    SELECT pages.page_id
    FROM pages
    WHERE NOT EXISTS (
        SELECT 1 FROM page_likes
        WHERE page_likes.page_id = pages.page_id
    )
) AS subquery;
```
**Execution Time:** ~3 minutes 45 seconds

### 4. Using `NOT EXISTS` with `LIMIT 1`
```sql
SELECT COUNT(*) FROM (
    SELECT pages.page_id
    FROM pages
    WHERE NOT EXISTS (
        SELECT 1 FROM page_likes
        WHERE page_likes.page_id = pages.page_id
        LIMIT 1
    )
) AS subquery;
```
**Execution Time:** ~3 minutes 45 seconds

### 5. Using `NOT IN`
```sql
SELECT COUNT(*) FROM (
    SELECT page_id
    FROM pages
    WHERE page_id NOT IN (
        SELECT page_id FROM page_likes
    )
) AS subquery;
```
**Execution Time:** Did not complete after **6+ hours**

## Results Summary
| Query Type | Execution Time |
|------------|---------------|
| `EXCEPT` | 14m 12s |
| `LEFT JOIN ... WHERE IS NULL` | 3m 44s |
| `NOT EXISTS` | 3m 45s |
| `NOT EXISTS` with `LIMIT 1` | 3m 45s |
| `NOT IN` | >6 hours (did not complete) |

## Conclusion
1. **`LEFT JOIN ... WHERE IS NULL` and `NOT EXISTS` with `LIMIT 1` performed the best (~3m 44s).**
2. **`EXCEPT` was significantly slower (~14m 12s).**
3. **`NOT EXISTS` without `LIMIT 1` performed similarly to `NOT EXISTS` with `LIMIT 1`.**
4. **`NOT IN` was the worst (did not complete in 6+ hours).**
5. **For cases with many duplicates, an optimized `EXCEPT` could perform better.**

## Recommendations
- **Use `LEFT JOIN ... WHERE IS NULL` or `NOT EXISTS` with `LIMIT 1` for large datasets.**
- **Avoid `NOT IN` for large datasets, as it can be extremely slow.**
- **Ensure `page_likes.page_id` is indexed for optimal performance.**

## Setup and Execution
### Prerequisites
- PostgreSQL database (tested on Amazon RDS `db.m5.xlarge`)
- 4 vCPUs, 16GB RAM
- Tables populated with 500M records each

### Running the Queries
1. Set up the database schema using the `CREATE TABLE` statements.
2. Populate the tables with **500M rows** each.
3. Run each query individually and note the execution time.
4. Compare performance and select the best approach for your use case.
