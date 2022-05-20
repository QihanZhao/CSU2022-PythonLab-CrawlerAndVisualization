import pymssql



conn = pymssql.connect(host='127.0.0.1',
                        user='sa',
                        password='010929',
                        database='pubs',
                        charset='utf8')
try:
    with  conn.cursor() as cursor:

        sql = "select * from titles"

        cursor.execute(sql)

        results = ''
        results = cursor.fetchall()
        print(results)
finally:
    conn.close()
