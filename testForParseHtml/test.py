# import requests

# def getHTMLText(url):
#     try:
#         r = requests.get(url, timeout=30)
#         r.raise_for_status()    #如果状态不是200OK，则引发HTTPError异常
#         r.encoding = r.apparent_encoding
#         return r.text
#     except:
#         return "产生异常"

# if __name__ == "__main__":
#     url = "http://www.baidu.com"
#     print(getHTMLText(url))

# eval("he:ll".split(":")[1])

from dataclasses import dataclass
from re import M

# m = 1
# def f():
#     return 1,2,3,
# a,b,c=f()
# print(a)
# print(b)
# print(c)

# m = 1
# def f():
#     print(m)
# f()

# d= {1:10,2:20}
# for k in d:
#     print(k)

# with open('data', 'r', encoding='utf-8') as f:
#     pass

import re

# html = '''<td>603260</td>
# <td class=tdred><a class=ared target="_blank" href="gpdm.asp?gpdm=603260">合盛硅业</a>'''
# for m in re.finditer(r'<a class=ared target="_blank" href=".*?">(.*?)</a>',
#                      html):
#     print(m)

# html = '''<td>603260</td>
# <td class=tdred><a class=ared target="_blank" href="gpdm.asp?gpdm=603260">合盛硅业</a>'''
# for m in re.finditer(r'gpdm\.asp\?gpdm=(\d{6})', html):
#     print(m)

html = '''<table class="tableQ" id="BIZ_hq_historySearch">
                            <thead>
                                <tr style="display:none">
                                    <td class="sum">累计：</td><td class="date" colspan="2"></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                                                                    </tr>
                                <tr style="display:none">
                                    <td class="e1"></td><td></td><td></td><td></td><td></td><td>105.91</td><td>105.91</td><td></td><td></td><td></td>
                                                                    </tr>
                                <tr class="bgGray1">
                                    <th class="e1">日期</th>
                                    <th class="e2">开盘</th>
                                    <th class="e3">收盘</th>
                                    <th class="e4">涨跌额</th>
                                    <th class="e5">涨跌幅</th>
                                    <th class="e6">最低</th>
                                    <th class="e7">最高</th>
                                    <th class="e8">成交量(手)</th>
                                    <th class="e9">成交金额(万)</th>
                                    <th>换手率</th>
                                                                    </tr>
                            </thead>
                            <tbody><tr style="">
                                    <td class="sum">累计：</td><td class="date" colspan="2">2022-01-17至2022-05-20</td><td>0.57</td><td>9.05%</td><td>5.55</td><td>7.03</td><td>26978164</td><td>1681546.27</td><td>14.99%</td>
                                                                    </tr><tr style="">
                                    <td class="e1">2022-04-25</td><td>6.25</td><td>6.05</td><td>-0.24</td><td>-3.82%</td><td>6.02</td><td>6.33</td><td>417636</td><td>25807.48</td><td>0.23%</td>
                                                                    </tr><tr style="">
                                    <td class="e1">2022-01-19</td><td>6.17</td><td>6.16</td><td>-0.05</td><td>-0.81%</td><td>6.12</td><td>6.20</td><td>218658</td><td>13458.19</td><td>0.12%</td>
                                                                    </tr><tr style="">
                                    <td class="e1">2022-01-18</td><td>6.13</td><td>6.21</td><td>0.08</td><td>1.31%</td><td>6.11</td><td>6.25</td><td>290596</td><td>17974.69</td><td>0.16%</td>
                                                                    </tr><tr style="">
                                    <td class="e1">2022-01-17</td><td>6.21</td><td>6.13</td><td>-0.17</td><td>-2.70%</td><td>6.11</td><td>6.22</td><td>326325</td><td>20073.91</td><td>0.18%</td>
                                                                    </tr></tbody>
                        </table>'''
'''
import bs4
htmlInBS = bs4.BeautifulSoup(html,"html.parser")
table = htmlInBS.find("table", attrs={"class": "tableQ", "id": "BIZ_hq_historySearch"})
body = table.find("tbody")
lst = body.contents
history30Data = []
for i in range(1,len(lst)):
    # print(lst[i])
    history1Data =[]
    for y in lst[i].contents:
        if  y.string[0].isdigit():
            history1Data.append(y.string)
    history30Data.append(history1Data)
print(history30Data)
'''
# print(body)

#对应<li><a href=" /gupiao/ 600151/">航天机电(600151)</a></li>

# codes.append(x.string)


# <table class="tableQ" id="BIZ_hq_historySearch">

# 成为bs对象后，字典的键和值都是字符串
# soup.a
# bs对象 存在某个属性
# bs4 ， re库的使用


# html = ""
# count =0
# # p = r'target="_blank" href=".*?">(.*?)</a>'
# p = r'''<tr  height="25">[^<]*<td>\d{1,3}</td>[^<]*<td>(\d{6})</td>[^<]*<td class=.*?><a.*?>(.*?)</a>'''
# for m in re.finditer(p, html):
#     print(m)
#     count +=1
# print(count)

# mylist=[['华兰生物', '002007', '医药制造'],
#     ['星宇股份', '601799', '汽车制造'],
#     ['芒果超媒', '300413', '文体传媒']
#     ]

# for s in mylist:
#     print(s[0])
#     # print("INSERT INTO stockList VALUES({},{},{})".format(s[0], s[1], s[2]))


def f(lst):
    lst[3]="hello"
    print(lst)

lst = [1,2,3,4,5]
f(lst)
print(lst)