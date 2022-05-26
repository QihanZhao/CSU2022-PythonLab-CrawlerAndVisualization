import re
import requests


# def getStockList2(listURL):
#     requests.request(listURL)
#     codes = []
#     html =
#     count = 0
#     # p = r'target="_blank" href=".*?">(.*?)</a>'
#     p = r'''<tr  height="25">\n<td>(\d)</td>\n\n<td>(\d{6})</td>\n<td class=tdred><a.*?>(.*?)</a>'''
#     for m in re.finditer(p, html):
#         print(m)
#         count += 1
#     print(count)
#     return codes

listURL = "http://www.shdjt.com/flsort.asp?lb=993505"
r = requests.get(url = listURL)
html = r.text
# p = r'''<tr  height="25">\n<td>(\d)</td>\n\n<td>(\d{6})</td>\n<td class=tdred><a.*?>(.*?)</a>'''
# p = r'''<tr  height="25">\r\n<td>\d{1,3}</td>\r\n\r\n<td>(\d{6})</td>\r\n<td .*?><a.*?>(.*?)</a>'''
# p = r'''<tr  height="25">\r\n<td>\d{1,3}</td>\r\n\r\n<td>(\d{6})</td>\r\n<td class=.*?><a.*?>(.*?)</a>'''
p = r'''<tr  height="25">[^<]*<td>\d{1,3}</td>[^<]*<td>(\d{6})</td>[^<]*<td class=.*?><a.*?>(.*?)</a>'''
# <tr  height="25">[^<]*<td>\d{1,3}</td>[^<]*<td>(\d{6})</td>[^<]*<td class=\.*?><a\.*?>(\.*?)</a>
# f = open("htmlOK.txt", "w")
# f.write(html)
# f.close()

# print(html.find("有色金属"))
count = 0
print(count)
for m in re.findall(p, html):
    print(m)
    count += 1
    print(count)
