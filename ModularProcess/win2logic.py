import ing

import asyncio
import pyppeteer as pyp
import bs4
import re
import pandas as pd
import mplfinance as mpf
from asyncio.windows_events import NULL
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

win = tk.Tk()
win.resizable(False, False)  #锁定大小

lsbStockList = NULL
treeStockInfo = NULL
lbKLine = NULL
img = NULL

stockList = []
page = NULL
historyInfo = []
loop = asyncio.get_event_loop()

# def change_image():
#     """Change background image of the window."""
#     img = ImageTk.PhotoImage(Image.open("KOsmall.png"))
#     lbKLine.config(image=img)
#     lbKLine.imag = img

def doubleClickinList(event):
    for i in treeStockInfo.get_children():
        treeStockInfo.delete(i)

    i = lsbStockList.curselection()
    print(i)
    infoTask = loop.create_task(
        ing.getStockInfo(stockList[i[0]], page, "https://q.stock.sohu.com/cn/"))
    loop.run_until_complete(infoTask)
    rawData = infoTask.result()

    tmpt = [(i[0:3] + i[5:7]) for i in rawData]
    for i in range(len(tmpt)):
        treeStockInfo.insert('', 'end', values=tmpt[i])

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

    individualURL = "https://q.stock.sohu.com/cn/"
    oneStockInfoList = await ing.getStockInfo(stockCodeList[2], page,
                                              individualURL)
    print(oneStockInfoList)

    ing.showOneKLineChart(oneStockInfoList)

    await browser.close()  #关闭浏览器


loop.run_until_complete(getStcockList())

#股票列表--------------------------------------------------------------
lsbStockList = tk.Listbox(win, width=40, height=32)
lsbStockList.grid(row=0, column=1, rowspan=2, padx=5, pady=20)
lsbStockList.bind("<Double-Button-1>", doubleClickinList)
for stock in stockList:
    lsbStockList.insert(
        tk.END,
        str("{0:{3}<8}{1:^10}{2:>14}".format(stock[0],stock[1],stock[2],chr(12288)))
        )

#K线图--------------------------------------------------------------
lbKLine = tk.Label(win)
img0 = ImageTk.PhotoImage(Image.open("welcome.png"))
lbKLine.config(image=img0)
lbKLine.grid(row=1, column=0, padx=5, pady=5)

#表格+滚动条--------------------------------------------------------------
frStockInfo = tk.Frame(win, )
frStockInfo.grid(row=0, column=0, padx=5, pady=5)

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
treeStockInfo.column('日期', anchor="center", width=95)  # 定义表头
treeStockInfo.column('开盘', anchor="center", width=95)  # 定义列
treeStockInfo.column('收盘', anchor="center", width=95)  # 定义列
treeStockInfo.column('最低', anchor="center", width=95)  # 定义列
treeStockInfo.column('最高', anchor="center", width=95)  # 定义列
treeStockInfo.grid(row=0, column=0, padx=5, pady=5, sticky="WENS")
# rawData=[
# ["2022-05-23",18.45,  18.55,  18.35,  18.75,  103659.0,],
# ["2022-05-23",18.40,  18.53,  18.40,  18.71,  113566.0,],
# ["2022-05-23",18.68,  18.98,  18.38,  19.02,  154463.0,],
# ["2022-05-23",19.65,  19.45,  19.12,  19.77,  185583.0,],
# ["2022-05-23",18.45,  18.55,  18.35,  18.75,  103659.0,],
# ["2022-05-23",18.40,  18.53,  18.40,  18.71,  113566.0,],
# ["2022-05-23",18.68,  18.98,  18.38,  19.02,  154463.0,],
# ["2022-05-23",19.65,  19.45,  19.12,  19.77,  185583.0,],
# ["2022-05-23",18.45,  18.55,  18.35,  18.75,  103659.0,],
# ["2022-05-23",18.40,  18.53,  18.40,  18.71,  113566.0,],
# ["2022-05-23",18.68,  18.98,  18.38,  19.02,  154463.0,],
# ["2022-05-23",19.65,  19.45,  19.12,  19.77,  185583.0,],
# ]
# data = [i[0:5] for i in rawData]
# for i in range(len(data)):
#     treeStockInfo.insert('', 'end', values=data[i])

scrollbar = tk.Scrollbar(frStockInfo,
                         width=15,
                         orient="vertical",
                         command=treeStockInfo.yview)
treeStockInfo.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky="NS")

win.mainloop()
