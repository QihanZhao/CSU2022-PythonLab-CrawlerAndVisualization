import asyncio
import pyppeteer as pyp
import bs4
import re
import pandas as pd
import mplfinance as mpf

from requests import request
import requests


#反反爬措施
async def antiAntiCrawler(page):
    await page.setUserAgent('Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
                                AppleWebKit/537.36 (KHTML,like Gecko) \
                                Chrome/78.0.3904.70 \
                                Safari/537.36')
    await page.evaluateOnNewDocument(' () =>{ object. defineProperties \
                                        (navigator, { webdriver:{ get: () => false } }) }'
                                     )


async def getStockList(page, listURL):
    await page.goto(listURL)  #装入url对应的网页
    codes = []
    html = await page.content()
    htmlInBS = bs4.BeautifulSoup(html, "html.parser")
    count = 0
    for x in htmlInBS.find_all("a",
                attrs={"target": "_blank","href":re.compile("^gpdm\.asp\?gpdm=(\d{6})")}):
        if (count == 28):
            break
        count += 1
        name = x.string
        href = x.attrs['href']
        code = re.search("gpdm\.asp\?gpdm=(\d{6})", href).group(1)
        industry = x.parent.parent.find("font").string
        codes.append([name, code, industry])
    return codes


def getStockList2(listURL):
    r = requests.get(url=listURL)
    html = r.text
    codes = []
    count = 0
    # p = r'target="_blank" href=".*?">(.*?)</a>'
    p = r'''<tr  height="25">[^<]*<td>\d{1,3}</td>[^<]*<td>(\d{6})</td>[^<]*<td class=.*?><a.*?>(.*?)</a>'''
    for m in re.finditer(p, html):
        print(m)
        count += 1
    print(count)
    return codes


async def getStockInfo(oneStock, page, stockURL):

    url = stockURL + oneStock[
        1] + "/lshq.shtml"  # oneStock[1] is the code of this stock
    print(url)
    await page.goto(url)
    html = await page.content()
    htmlInBS = bs4.BeautifulSoup(html, "html.parser")
    table = htmlInBS.find("table",
                          attrs={"class": "tableQ","id": "BIZ_hq_historySearch"})
    body = table.find("tbody")
    lst = body.contents
    history30Data = []
    for i in range(1, 31):
        history1Data = []
        for y in lst[i].contents:
            if (y.string[0].isdigit() or y.string[0] == "-"):
                history1Data.append(y.string)
        history30Data.append(history1Data)
    print(len(history30Data))
    return history30Data


def showOneKLineChart(rawData):
    data = [(i[1:3] + i[5:8]) for i in rawData]
    dataNumber = []
    for line in data:
        # print(line)
        dataNumber.append([float(x) for x in line])
    print(dataNumber)
    index = [i[0] for i in rawData]
    index = pd.DatetimeIndex(index)

    columns = ['Open', 'Close', 'Low', 'High', 'Volume']
    daily = pd.DataFrame(dataNumber, columns=columns, index=index)
    daily.index.name = 'Date'

    print(daily)

    # mpf.plot(daily)
    mpf.plot(daily,
             type='candle',
             mav=(3, 6, 9),
             volume=True,
             savefig=dict(fname='KOsmall', dpi=60))


async def main():

    browser = await pyp.launch(headless=False,
                               executablePath="D:/chrome-win/chrome.exe",
                               userdataDir="D:/tmpForCrawler"
                               )  #启动Chromium , browser即为Chromium浏览器，非隐藏启动
    page = await browser.newPage()  #在浏览器中打开一个新页面(标签)
    await antiAntiCrawler(page)  #新页面生成后一律调用此来反反爬

    listURL = "http://www.shdjt.com/flsort.asp?lb=993505"
    stockCodeList = await getStockList(page, listURL)
    # stockCodeList = getStockList2(listURL)
    print(stockCodeList)

    individualURL = "https://q.stock.sohu.com/cn/"
    oneStockInfoList = await getStockInfo(stockCodeList[2], page,
                                          individualURL)
    print(oneStockInfoList)

    showOneKLineChart(oneStockInfoList)

    await browser.close()  #关闭浏览器


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    mainTask = loop.create_task(main())
    loop.run_until_complete(mainTask)
    # main()
