from asyncio.windows_events import NULL
import pymssql


stockList = []
conn = NULL

def makeConn():
    global conn
    conn = pymssql.connect(host='127.0.0.1',
                           user='sa',
                           password='010929',
                           database='stocks',
                           charset='utf8')

def getStockList():

    global stockList
    global conn

    makeConn()
    try:
        with conn.cursor() as cursor:

            sql = "select * from stockList"

            cursor.execute(sql)

            stockList = cursor.fetchall()
            # print(stockList)
    finally:
        conn.close()


def storeStockList():
    global conn

    makeConn()
    try:
        with conn.cursor() as cursor:

            sql = "INSERT INTO stockList VALUES(?,?,?)"

            # mylist=[['华兰生物', '002007', '医药制造'],
            #         ['星宇股份', '601799', '汽车制造'],
            #         ['芒果超媒', '300413', '文体传媒']
            #         ]
            mylist = stockList

            for s in mylist:
                # print(s[0])
                cursor.execute("INSERT INTO stockList VALUES(%s,%s,%s)",
                               (s[0], s[1], s[2]))
                print((s[0], s[1], s[2]))

            conn.commit()

    except pymssql.DatabaseError:
        print("error")
        conn.rollback()
    finally:
        print("success")
        conn.close()



# storeStockList()