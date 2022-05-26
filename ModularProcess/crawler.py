import asyncio
from xml.sax.xmlreader import AttributesImpl
import pyppeteer as pyp
import bs4
import re

#反反爬措施
async def antiAntiCrawler(page):
    await page.setUserAgent ( 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
                                AppleWebKit/537.36 (KHTML,like Gecko) \
                                Chrome/78.0.3904.70 \
                                Safari/537.36'                                                                                                                                                                                                                                                                                    )
    await page.evaluateOnNewDocument (' () =>{ object. defineProperties \
                                        (navigator, { webdriver:{ get: () => false } }) }'                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            )

#索引集合获取：3种实现---------------------------------------------------
# #正则表达式耗时：0:00:00.033943
# async def getStockCodes(page) :
#     #从"https://www.banban.cn/gupiao/list_sh.html"对应的page获取所有股票名称和代码
#     codes=[]
#     #最终内容: [" 四川路桥(600039) " , "包钢股份(600010)"......]
#     html = await page.content()
#     pt = '<a href="/gupiao/\d*/">([^<]*\(\d+\))</a>'
#     #对应<li><a href=" /gupiao/600151/">航天机电(600151)</a></li>
#     for x in re.findall (pt ,html) :
#         codes.append (x)
#     return codes

#BeautifulSoap耗时: 0:00:00.193480
async def getStockCodes(page) :
    codes=[]
    html = await page.content()
    htmlInBS = bs4.BeautifulSoup(html,"html.parser")
    for x in htmlInBS.find_all("a", attrs={"class": "ared", "target": "_blank"}):
        #对应<li><a href=" /gupiao/ 600151/">航天机电(600151)</a></li>
        codes.append(x.string)
    return codes

# #pyppeteer耗时: 0:00:04.421178
# async def getStockCodes (page) :
#     codes = [ ]
#     elements = await page.querySelectorAll ("li") #根据tag name找元素
#     #对应<li><a href="/gupiao/600151/">航天机电(600151)</a></li>
#     for e in elements :
#         a = await e.querySelector ("a") #根据tag name找元素
#         obj = await a.getProperty ("innerText" )  #还可以a.getProperty ("href")
#         text = await obj.jsonvalue() #固定写法
#         if("("in text and ")" in text):
#             codes.append (text)
#     return codes
#------------------------------------------------------------------------

async def getStockInfo(url):
    browser = await pyp.launch(headless=False,
                               executablePath="D:/chrome-win/chrome.exe",
                               userdataDir="D:/tmpForCrawler"
                               )  #启动Chromium , browser即为Chromium浏览器，非隐藏启动
    page = await browser.newPage()    #在浏览器中打开一个新页面(标签)
    await antiAntiCrawler (page)    #新页面生成后一律调用此来反反爬
    await page.goto (url)    #装入url对应的网页
    #------------------------------------------------------
    codes = await getStockCodes (page)
    #------------------------------------------------------
    for x in codes[ :3] :   #只取前三个股票信息
        print("-----" ,x)   #x形如"四川路桥(600039)"
        # pos1, pos2 = x.index("("), x.index(")")
        # code =x [pos1 + 1 :pos2] #取股票代码,如600039
        # url = "https://quote.eastmoney.com/sh" + code + ".html"
        # await page.goto (url)
        # html = await page.content() #往下编程前可以先print (html)看一看
        # pt = '<td>([^<]*)</td>.*?<td[^>]*id= ="gt\d*?"[^>]*>([^<]*)</td> '
        # for x in re. findall (pt,html, re.DOTALL) :
        #     print(x[0] ,x[1])
    #------------------------------------------------------
    await browser.close ()    #关闭浏览器


url = "http://www.shdjt.com/flsort.asp?lb=993505"
loop = asyncio.get_event_loop()
loop.run_until_complete (getStockInfo (url))