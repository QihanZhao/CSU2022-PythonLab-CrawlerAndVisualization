import ing

import pymssql
import asyncio
import pyppeteer as pyp
from asyncio.windows_events import NULL

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

stockList = []
page = NULL
historyInfo = []
loop = asyncio.get_event_loop()

win = tk.Tk()
win.resizable(False, False)  #锁定大小

lsbStockList = NULL
treeStockInfo = NULL
lbKLine = NULL
img = NULL
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
    finally:
        conn.close()


def storeHistoryData():
    global conn
    global historyInfo
    makeConn()
    try:
        with conn.cursor() as cursor:
            for s in historyInfo:
                # print(s[0])
                cursor.execute(
                    "INSERT INTO historyData VALUES(%s,%s,%s,%s,%s)",
                    (s[0], s[1], s[2], s[3], s[4]))
                print((s[0], s[1], s[2], s[3], s[4]))
            conn.commit()
    except pymssql.DatabaseError:
        print("error")
        conn.rollback()
    finally:
        print("success")
        conn.close()


def readHistoryData():
    global conn
    global historyInfo
    makeConn()
    try:
        with conn.cursor() as cursor:
            sql = "select * from historyData"
            cursor.execute(sql)
            historyInfo = cursor.fetchall()
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(historyInfo)
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    finally:
        conn.close()


def deleteHistoryData():
    global conn
    makeConn()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM historyData")
            conn.commit()
    except pymssql.DatabaseError:
        print("error")
        conn.rollback()
    finally:
        print("success")
        conn.close()


def doubleClickinList(event):
    global historyInfo
    #删除上一次点击的公司 数据库 和 GUI表格 的数据
    deleteHistoryData()
    for i in treeStockInfo.get_children():
        treeStockInfo.delete(i)

    i = lsbStockList.curselection()
    # print(i)
    infoTask = loop.create_task(
        ing.getStockInfo(stockList[i[0]], page,
                         "https://q.stock.sohu.com/cn/"))
    loop.run_until_complete(infoTask)
    rawData = infoTask.result()
    historyInfo = [(i[0:3] + i[5:7]) for i in rawData]

    storeHistoryData()

    historyInfo = []
    readHistoryData()
    print("------------------------------------------------------------")
    print(historyInfo)
    print("------------------------------------------------------------")
    for i in range(len(historyInfo)):
        treeStockInfo.insert('', 'end', values=historyInfo[i])

    img = ImageTk.PhotoImage(Image.open("KOsmall.png"))
    lbKLine.config(image=img)
    lbKLine.imag = img

    ing.showOneKLineChart(rawData)


async def getStcockList():
    global page
    global stockList
    browser = await pyp.launch(headless=False,
                               executablePath="D:/chrome-win/chrome.exe",
                               userdataDir="D:/tmpForCrawler"
                               )  #启动Chromium , browser即为Chromium浏览器，非隐藏启动
    page = await browser.newPage()  #在浏览器中打开一个新页面(标签)
    await ing.antiAntiCrawler(page)  #新页面生成后一律调用此来反反爬

    listURL = "http://www.shdjt.com/flsort.asp?lb=993505"
    stockList = await ing.getStockList(page, listURL)
    # stockCodeList = getStockList2(listURL)
    return


loop.run_until_complete(getStcockList())

getStockList()
if len(stockList) == 0:
    conn = pymssql.connect(host='127.0.0.1',
                           user='sa',
                           password='010929',
                           database='stocks',
                           charset='utf8')
    try:
        with conn.cursor() as cursor:
            for s in stockList:
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

#股票列表--------------------------------------------------------------
lsbStockList = tk.Listbox(win, width=40, height=32)
lsbStockList.grid(row=0, column=1, rowspan=2, padx=5, pady=20)
lsbStockList.bind("<Double-Button-1>", doubleClickinList)
for stock in stockList:
    lsbStockList.insert(
        tk.END,
        str("{0:{3}<8}{1:^10}{2:>14}".format(stock[0], stock[1], stock[2],
                                             chr(12288))))

#K线图--------------------------------------------------------------
lbKLine = tk.Label(win)
img0 = ImageTk.PhotoImage(Image.open("welcome.png"))
lbKLine.config(image=img0)
lbKLine.grid(row=1, column=0, padx=5, pady=5)

#表格+滚动条--------------------------------------------------------------
frStockInfo = tk.Frame(win, )
frStockInfo.grid(row=0, column=0, padx=5, pady=5)
#表格
columns = ['日期', '开盘', '收盘', '最低', '最高']
treeStockInfo = ttk.Treeview(
    frStockInfo,  # 父容器
    height=10,  # 表格显示的行数,height行
    columns=columns,  # 显示的列
    show='headings',  # 隐藏首列
)
treeStockInfo.heading(
    '日期',
    text='日期',
)  # 定义表头
treeStockInfo.heading(
    '开盘',
    text='开盘',
)  # 定义表头
treeStockInfo.heading(
    '收盘',
    text='收盘',
)  # 定义表头
treeStockInfo.heading(
    '最低',
    text='最低',
)  # 定义表头
treeStockInfo.heading(
    '最高',
    text='最高',
)  # 定义表头
treeStockInfo.column('日期', anchor="center", width=95)  # 定义列
treeStockInfo.column('开盘', anchor="center", width=95)  # 定义列
treeStockInfo.column('收盘', anchor="center", width=95)  # 定义列
treeStockInfo.column('最低', anchor="center", width=95)  # 定义列
treeStockInfo.column('最高', anchor="center", width=95)  # 定义列
treeStockInfo.grid(row=0, column=0, padx=5, pady=5, sticky="WENS")
#滚动条
scrollbar = tk.Scrollbar(frStockInfo,
                         width=15,
                         orient="vertical",
                         command=treeStockInfo.yview)
treeStockInfo.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky="NS")

win.mainloop()
