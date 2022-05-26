import asyncio
import pyppeteer as pyp
import re


#反反爬措施
async def antiAntiCrawler(page):
    await page.setUserAgent('Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
                                AppleWebKit/537.36 (KHTML,like Gecko) \
                                Chrome/78.0.3904.70 \
                                Safari/537.36'                                                                                                                                                                                                                                                                                                                                                                                                                                                                            )
    await page.evaluateOnNewDocument(' () =>{ object. defineProperties \
                                        (navigator, { webdriver:{ get: () => false } }) }'
                                     )


async def getStockInfo(url):
    browser = await pyp.launch(headless=False,
                               executablePath="D:/chrome-win/chrome.exe",
                               userdataDir="D:/tmpForCrawler"
                               )  #启动Chromium , browser即为Chromium浏览器，非隐藏启动
    page = await browser.newPage()  #在浏览器中打开一个新页面(标签)
    # await antiAntiCrawler(page)  #新页面生成后一律调用此来反反爬
    await page.goto(url)  #装入url对应的网页
    #------------------------------------------------------
    html = await page.content()
    f = open("htmlERROR.txt", "w")
    f.write(html)
    f.close()
    count = 0
    for m in re.findall(
            r'<tr height="25">[^<]*<td>\d{1,3}</td>[^<]*<td>(\d{6})</td>[^<]*<td class=.*?><a.*?>(.*?)</a>',
            html):
        print(m)
        count += 1
    print(count)
    #------------------------------------------------------
    await browser.close()  #关闭浏览器


url = "http://www.shdjt.com/flsort.asp?lb=993505"
loop = asyncio.get_event_loop()
loop.run_until_complete(getStockInfo(url))
