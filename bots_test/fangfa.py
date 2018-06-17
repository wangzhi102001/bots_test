from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError,URLError
from time import sleep
import json
import datetime
import time
import re
import requests

def getLinksFrom_Ban(date,url_ban,headers):
    '''从BS对象获取整版所有新闻链接尾的列表'''
    if url_ban != None:
        bsObj = getbsObj(url_ban,headers)
    urls_news_part = []
    if bsObj != None:
        for link in bsObj.findAll("area"):
            if 'href' in link.attrs:
                urls_news_part.append("http://cdrb.cdyee.com/html/%s-%s/%s/" % (date[:4],date[5:7],date[-2:]) + link.attrs['href'])
    return urls_news_part



def getText(url,headers):
    '''通过url获取包含新闻主标题、副标题、内容的字典'''
    
    bsObj = getbsObj(url,headers)
    if bsObj != None:
        title_one_news = bsObj.find("td",{"class":"bt1"})
        title_two_news = bsObj.find("td",{"class":"bt2"})
        content_news = bsObj.find("td",{"class":"xilan_content_tt"})
    else:
        return {'link':'','bt1':'','bt2':'','body':''}
    #news =
    #{'link':url,'bt1':title_one_news.get_text(),'bt2':title_two_news.get_text(),'content':content_news.get_text()}
    news = {'link':url,'bt1':title_one_news,'bt2':title_two_news,'body':content_news}
    sleep(0.5)
    return news

def findWithDate(date,urls_ban,urls_news,headers):
    '''通过日期获取所有新闻的链接'''
   

    for i in range(0,10):
        url_temp = "http://cdrb.cdyee.com/html/%s-%s/%s/node_%d.htm" % (date[:4],date[5:7],date[-2:],i)
        urls_ban.append(url_temp)
    for url in urls_ban.copy():
        if url != None:
            urls_news+= getLinksFrom_Ban(date,url,headers)
    return urls_news

def getbsObj(url,headers):
    '''验证url是否可用，并返回bs对象'''
    try:    
        html = urlopen(url)
    except HTTPError as e:
        print("%s无法连接，继续下一个" % url)
        return None
    try:
        session = requests.Session()
        req = session.get(url,headers = headers)
        bsObj = BeautifulSoup(req.text,"lxml")
    except AttributeError as e:
        return None
    return bsObj

def typeDate(news):
    news_typed = {}
    news_typed['link'] = news['link']
    news_typed['bt1'] = news['bt1'].get_text()
    if news['bt2'] != '':
        news_typed['bt2'] = news['bt2'].get_text()
    else:
        news_typed['bt2'] = ''

    news_typed['body'] = news['body'].get_text().replace('\xa0',' ')
    return news_typed
    


def saveToTxt(news,filename):
    with open(filename,'a',errors='ignore') as f_obj:
        
        f_obj.write(str(news['link']) + '\n')
        f_obj.write(str(news['bt1']) + '\n')
        f_obj.write(str(news['bt2']) + '\n')
        f_obj.write(str(news['body']) + '\n')
        f_obj.write('\n')
        
def saveToJson(list,filename):
    with open(filename,'w') as f:
        f.write(json.dumps(list,ensure_ascii=False)+"\n")


def date_add(date):
    new_date = datetime.datetime.strptime(date,"%Y-%m-%d") + datetime.timedelta(days = 1)
    new_date_formated = datetime.datetime.strftime(new_date,'%Y-%m-%d')
    return new_date_formated

def screeningUrl(urls_news,keyword,headers):
    '''关键词筛选'''
    newurls = []
    news = {}
    for url in urls_news:
        news = getText(url,headers)
        if news['bt1'] != None:
            if keyword in news['bt1']:
                newurls.append(url)
            if keyword in news['bt2'] and url not in newurls:
                newurls.append(url)
            if keyword in news['body'] and url not in newurls:
                newurls.append(url)
    newurls = list(set(newurls))

    return newurls


def getdate():
    while True:
        r = "(([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))|((([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00))-02-29)"
        date_input = input("请输入查询起始日期（例如“2018-04-01”）")
        if re.match(r,date_input):
            return date_input
            break
        

def getdays():
   while True:
        r = "[0-9]*3"
        days = input("请输入小于300的整数")
        if re.match(r,days) and int(days) <= 300 and int(days) > 0:
            return int(days)
        else:
            continue

def is_valid_date(str):
    '''判断是否是一个有效的日期字符串'''
    try:
        time.strptime(str, "%Y-%m-%d")
        return True
    except:
        return False        

def make_path(filename,link):
    newfilename = str.replace(link[str.find(link,'l/') + 2:str.find(link,'l/') + 12],'/','-')+filename
    return newfilename
 