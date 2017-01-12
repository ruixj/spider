# -*- coding: UTF-8 -*-
import urllib
import urllib2
import cookielib
import json
import string
import re
import time
import os
#import md5
import hashlib

APPKEY = "04a13318bc680b9e4da7bba876224a95"
FIREFOX= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'

def getsign(appkey,apiname):
    src = apiname+appkey
    m1  = hashlib.md5()
    m1.update(src)
    return m1.hexdigest()

def login(loginName,loginPwd):
    filename = 'cookie.txt'
    cookie = cookielib.MozillaCookieJar(filename)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    postdata = urllib.urlencode({
                'user_name':loginName,
                'password':loginPwd
            })

    signkey = getsign(APPKEY,'account')

    loginUrl = 'http://wc.lelianyanglao.com/api/account/login_process/?mobile_sign='+signkey
    print loginUrl
    result = opener.open(loginUrl,postdata)
    cookie.save(ignore_discard=True, ignore_expires=True)
    loginres = result.read()
    return loginres 

def postarticle(title,content):
    cookie = cookielib.MozillaCookieJar()
    cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)

    #user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

    values = {'title':title,
              'message':content,
              'category_id':1
             }

    #headers = {'User-Agent':user_agent}
    data    = urllib.urlencode(values)
    
    signkey = getsign(APPKEY,'publish')


    publishUrl = 'http://wc.lelianyanglao.com/api/publish/publish_article/?mobile_sign='+signkey
    print publishUrl
    req = urllib2.Request(publishUrl,data)

    #req.add_header('User-agent',FIREFOX)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    response = opener.open(req)
    #print response.read() 
    return response.read()

def geturls(start_id,page_size,page_num):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    values = {'start_id':start_id,
              'page_size':page_size,
              'p':page_num
             }
    headers = {'User-Agent':user_agent}
    data    = urllib.urlencode(values)
    try:
        req = urllib2.Request('http://m.lelianyanglao.com/index.php?m=api&a=get_splider_list',data,headers)
        response = urllib2.urlopen(req)
        urls = response.read()
        return urls 
    except urllib2.URLError,e:
        if hasattr(e,"reason"):
            print u"unable to get the urls"
            return None

def getPageContent(url):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headersL = {'User-Agent':user_agent}
    try:    
        req = urllib2.Request(url,headers=headersL)
        response = urllib2.urlopen(req)
        page = response.read()
        return page 
    except urllib2.URLError,e:
        if hasattr(e,"reason"):
            print u"Fail to get page from ",url
            return None

def getImagesInWxPage(page):
    if not page:
        print u"invalid page"

    wxpsoup = BeaufifulSoup(page)
    #1. find img 
    #wxpsoup.find_all("img",data-src=True)

    #2. store it into cloud and get the url of the img
    #3. replace the img src in the page with the url
    #4. return new page
   
def mkdir(path):
    path = path.strip()
    isExists = os.path.exists(path)
    if not isExists:
        print u"creating folder",path
        os.makedirs(path)
        return True 
    else:
        print "folder ",path," already exists"
        return False


def savePage(name,content):
    fileName = name + "/" + name + ".html"
    f = open(fileName,"w+")
    print u"Saving page", name
    f.write(content)


def main_process():
    start_id = 0;
    jsonUrlsStr= geturls(start_id,20,1)
    if jsonUrlsStr:
       jsonUrlObj = json.loads(jsonUrlsStr)

       if (jsonUrlObj["result"]["code"] == "OK"):
            reccount     = jsonUrlObj["data"]["data_recode_count"]
            #rec_count    = int(reccount)
            record_count = string.atoi(reccount);

            if(record_count > 0):
                start_id += record_count
                recordlist = jsonUrlObj["data"]["data_record_list"]
                for record in recordlist:
                    print record["link_url"],'\n'
                    pageContent = getPageContent(record["link_url"])
                    
                    title = record["title"]
                    #mkdir(title)
                    #savePage(title,pageContent)
                    login("tangzhen","123456")
                    #postarticle(title,pageContent)
                    
if __name__ == '__main__':
    print u"你好世界" 
    #while True:
    #    time.sleep(60*60)

    res = login('tangzhen','123456')

    print res

    res = postarticle('from python','from python')
    print res
