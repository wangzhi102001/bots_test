from bs4 import BeautifulSoup
from urllib.request import urlopen
import fangfa as ff
from time import sleep
import json
import time
import requests
#date = input("请输入日期，格式'20180404'")

session = requests.Session()
headers = {
   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134","Accrpt":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
headers_two = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36","Accrpt":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
urls_bans = []
urls_news = []
file_name = 'new.txt'
json_name = 'new.json'
date_need = ''
length = 0
js_list = []
keyword = ''
links = []
b = True
title_one_news = ""
title_two_news = ""
content_news = ""
num = 1

#while True and num>=0:
#    date_need = ff.getdate(b)
#    links_before = ff.findWithDate(date_need,urls_bans,urls_news)
#    print(r"%s:共获取,%d条信息链接"% (date_need,len(links_before)))
#    if input("是否启用关键字筛选链接（Y/N）").lower()=='y'and b:
#        keyword =input("请输入关键词")
#        print(r"%s:正在查询,包含关键词%s的链接"% (date_need,keyword))
#        links+=ff.screeningUrl(links_before.copy(),keyword)
#        print(r"%s:共查询出包含关键词%s的链接%d条"% (date_need,keyword,len(links)))
#    if input("是否使用下一日期查询（Y/N）").lower()=='y'and b:
#        date_need = ff.date_add(date_need)
#        b =False
#        continue
#    else:
#        if input("是否按照天数进行循环查询（Y/N").lower() == 'y':
#            num = ff.getdays()
#            date_need = ff.date_add(date_need)
#            num-=1
#            b = False
#    if input("是否开始下载（Y/N）").lower()=='y':
#        break
date_need = ff.getdate()
while True and num >= 0:   
    
    links_before = ff.findWithDate(date_need,urls_bans,urls_news,headers)
    print(r"%s:共获取,%d条信息链接" % (date_need,len(links_before)))
    #keyword ='城头山'
    #print(r"%s:正在查询,包含关键词%s的链接"% (date_need,keyword))
    #links+=ff.screeningUrl(links_before.copy(),keyword,headers)
    #print(r"%s:共查询出包含关键词%s的链接%d条"% (date_need,keyword,len(links)))
    links = links_before
    #num = 120
    date_need = ff.date_add(date_need)
    num-=1
    



        

for link in links[:]:
    
    if ff.getText(link,headers)['bt1'] != '':
        content = ff.typeDate(ff.getText(link,headers))
    else:
       continue
    if content['bt1'] != '':
        js_list.append(content)
        ff.saveToTxt(content,ff.make_path(file_name,link))
        length+=1
        print('%s已写入' % link)
        sleep(0.5)
    if length >= 40:
        sleep(1)
        length = 0

ff.saveToJson(js_list,ff.make_path(json_name,link))
print('全部完成，共写入%s条新闻信息' % len(js_list))







