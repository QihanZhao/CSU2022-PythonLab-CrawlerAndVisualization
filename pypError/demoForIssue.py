import asyncio
import pyppeteer

async def getStockInfo(url):
    browser = await pyppeteer.launch(headless=False,
                               executablePath="D:/chrome-win/chrome.exe",
                               userdataDir="D:/tmpForCrawler"
                               )  
    page = await browser.newPage()
    await page.goto(url)  
    #------------------------------------------------------
    html = await page.content()
    f = open("htmlERROR.txt", "w")
    f.write(html)
    f.close()
    #------------------------------------------------------
    await browser.close()  #关闭浏览器


url = "http://www.shdjt.com/flsort.asp?lb=993505"
loop = asyncio.get_event_loop()
loop.run_until_complete(getStockInfo(url))
