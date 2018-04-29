from bs4 import BeautifulSoup
from urllib.request import urlopen
import fangfa as ff
from time import sleep
import json
import time
#date = input("请输入日期，格式'20180404'")
urls_bans =[]
urls_news = []
file_name = 'new.txt'
json_name = 'new.json'
date_need = ''
length =0
js_list = []
keyword = ''
links=[]
b = True
num =120

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
while True and num>=0:   
    date_need = ff.getdate(b)
    links_before = ff.findWithDate(date_need,urls_bans,urls_news)
    print(r"%s:共获取,%d条信息链接"% (date_need,len(links_before)))
    keyword ='城头山'
    print(r"%s:正在查询,包含关键词%s的链接"% (date_need,keyword))
    links+=ff.screeningUrl(links_before.copy(),keyword)        
    print(r"%s:共查询出包含关键词%s的链接%d条"% (date_need,keyword,len(links)))
    #num = 120
    date_need = ff.date_add(date_need)
    num-=1
    b = False



        

for link in links:
    content = ff.typeDate(ff.getText(link))
    if content['bt1']!='':
        js_list.append(content)
        ff.saveToTxt(content,file_name)
        length+=1
        print('%s已写入' % link)
        sleep(1)
    if length>=40:
        #sleep(0.5)
        length = 0

ff.saveToJson(js_list,json_name)
print('全部完成，共写入%s条新闻信息' % len)







