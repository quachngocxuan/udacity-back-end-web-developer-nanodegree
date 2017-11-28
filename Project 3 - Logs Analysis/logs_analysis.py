#!/usr/bin/env python

import psycopg2


def connectDB():
    hostname = 'localhost'
    username = 'fullstack'
    password = 'fullstack'
    database = 'news'

    try:
        conn = psycopg2.connect(
            host=hostname,
            user=username,
            password=password,
            database=database)

        cursor = conn.cursor()

        return conn, cursor
    except Exception as error:
        print("Error in connecting to DB: " + error)


def queryAll(cursor, sql):

    try:
        cursor.execute(sql)

        return cursor.fetchall()
    except Exception as error:
        print("Execute the SQL: '" + sql + "' with error: " + error)


def closeDB(conn):
    try:
        conn.close()
    except Exception as error:
        print("Error in closing DB connection: " + error)


def getMostPopularArticles(cursor):
    sql = "SELECT a.title, l.count FROM articles a, \
        (SELECT path, COUNT(*) AS count FROM log GROUP BY path) l \
        WHERE CONCAT('/article/', a.slug)=l.path \
        ORDER BY l.count DESC \
        LIMIT 3"
    results = queryAll(cursor, sql)
    for result in results:
        print("\"" + str(result[0]) + "\" - " + str(result[1]) + " views")


def getMostPopularAuthors(cursor):
    sql = "SELECT at.name, ar.sum FROM authors at, \
        (SELECT a.author, SUM(l.count) AS sum FROM articles a, \
        (SELECT path, COUNT(*) AS count FROM log GROUP BY path) l \
        WHERE CONCAT('/article/', a.slug)=l.path \
        GROUP BY a.author) ar \
        WHERE at.id=ar.author \
        ORDER BY ar.sum DESC \
        LIMIT 5"
    results = queryAll(cursor, sql)
    for result in results:
        print(str(result[0]) + " - " + str(result[1]) + " views")


def getDaysWithLotsErrors(cursor):
    """
    Do this query by reference
    https://stackoverflow.com/questions/2099198/sql-transpose-rows-as-columns
    """

    sql = "SELECT l.day, l.count, l.fail_count \
        FROM (SELECT to_char(time, 'Mon DD, YYYY') AS day, \
            COUNT(*) AS count, \
            COUNT(CASE WHEN status='404 NOT FOUND' THEN id ELSE NULL END) \
                AS fail_count \
            FROM log GROUP BY day) l \
        WHERE l.fail_count::float/l.count > 0.01"
    results = queryAll(cursor, sql)
    for result in results:
        p = round(float(result[2])/result[1]*100, 2)
        print(result[0] + " - " + str(p) + "%")


def main():
    (conn, cursor) = connectDB()

    print("List of most popular articles:")
    getMostPopularArticles(cursor)

    print("List of most popular authors:")
    getMostPopularAuthors(cursor)

    print("List of days having error rate above 1%:")
    getDaysWithLotsErrors(cursor)

    closeDB(conn)


if __name__ == '__main__':
    main()
