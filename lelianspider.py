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
from html2ubb import *
import bs4
from bs4 import BeautifulSoup
from putimg2alioss import * 
from extractor import *

APPKEY   = "04a13318bc680b9e4da7bba876224a95"
FIREFOX  = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
FIREFOX2 = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

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
    
    #send the request to the url
    req = urllib2.Request(loginUrl,postdata)
    req.add_header('User-agent',FIREFOX)
    #result = opener.open(loginUrl,postdata)
    result = opener.open(req)
    
    cookie.save(ignore_discard=True, ignore_expires=True)
    
    loginres = result.read()
    return loginres 

def postarticle(title,content):
    cookie = cookielib.MozillaCookieJar()
    cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)

    print title
    #title   = urllib.quote(title)
    title    = title.encode('utf-8')
    print title
 
    #content = Html2UBB(content)
    #content = urllib.quote(content)
    content = content.encode('utf-8')

    values = {'title':title,
              'message':content,
              'category_id':1
             }

    data    = urllib.urlencode(values)
    
    signkey = getsign(APPKEY,'publish')
    publishUrl = 'http://wc.lelianyanglao.com/api/publish/publish_article/?mobile_sign='+signkey
    print publishUrl
    
    req = urllib2.Request(publishUrl,data)
    req.add_header('User-agent',FIREFOX)

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    response = opener.open(req)
    return response.read()

def geturls(start_id,page_size,page_num):
 
    values = {'start_id':start_id,
              'page_size':page_size,
              'p':page_num
             }
    headers = {'User-Agent':FIREFOX}
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
    print url 
    headersL = {'User-Agent':FIREFOX}
    try:    
        req = urllib2.Request(url,headers=headersL)
        response = urllib2.urlopen(req)
        page = response.read()
        return page 
    except urllib2.URLError,e:
        if hasattr(e,"reason"):
            print u"Fail to get page from ",url
            return None

def getImgWithSrc(page,pageSeq):
    if not page:
        print u"invalid page"

    wxpsoup = BeautifulSoup(page)
    #getTextAndImg(wxpsoup)
    #1. find img 
    datasrcImgList = wxpsoup.find_all("img",attrs={'src': True})
    imgSeq = 1
    for img in datasrcImgList:
        imgurl = img['src']
        imgExt = 'jpg'  #getImgExt(imgurl)
        imgName = getImgName(pageSeq,'src',imgSeq,imgExt)
        if imgurl == '':
            imgSeq += 1
            continue

        if(not checkUrlWithHttp(imgurl)):
            imgurl = "http:" + imgurl

        #print imgurl
        resurl = storeImg2AliOss(imgurl,imgName)
        #print resurl
        img['src'] = resurl
        imgSeq += 1

    return wxpsoup.prettify()


def getWxImgInPage(page,pageSeq,attr):
    if not page:
        print u"invalid page"

    wxpsoup = BeautifulSoup(page)
    #getTextAndImg(wxpsoup)
    #1. find img 
    datasrcImgList = wxpsoup.find_all("img",attrs={attr: True})
    imgSeq = 1
    for img in datasrcImgList:
        imgurl = img[attr]
        imgExt = getImgExt(imgurl)
        imgName = getImgName(pageSeq,attr,imgSeq,imgExt)
        #print 'before checking img url', imgurl
        if(not checkUrlWithHttp(imgurl)):
            imgurl = "http:" + imgurl

        resurl = storeImg2AliOss(imgurl,imgName)
        #print resurl
        img['src'] = resurl
        imgSeq +=1

    return wxpsoup.prettify()


    #     
    #2. store it into cloud and get the url of the img
    #3. replace the img src in the page with the url
    #4. return new page
    
def getWxImage2Local(url):
    headersL = {'User-Agent':FIREFOX}
    imgTypeReg = re.compile(r'wx_fmt=(.*)') 
    #try:    
        #req = urllib2.Request(url,headers=headersL)
        #response = urllib2.urlopen(req)
        #page = response.read()
         
    #except urllib2.URLError,e:
    #    if hasattr(e,"reason"):
    #        print u"Fail to get page from ",url
    #        return None


def getTextAndImg(page):
    wxsoup = BeautifulSoup(page,'html.parser')
    bodyElem = wxsoup.body
    #print bodyElem.prettify()
    #print bodyElem.contents[0]
    #loop through the children
    newsoup = BeautifulSoup('')
    btagnew = newsoup.new_tag('div')
    newsoup.append(btagnew) 
    #processChildren2(bodyElem,btagnew,newsoup)
    processChildren(bodyElem,btagnew,newsoup)

    return newsoup.prettify()

def getBodyWithoutScript(page):
    wxsoup = BeautifulSoup(page)
    content = ''
    scripts= wxsoup.find_all("script")
    for script in scripts:
        script.decompose()

    content = str(wxsoup.body)
    return content
                
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
    content = content.encode('utf-8')
    f.write(content)


def loop_body(last_startid):
    jsonUrlsStr= geturls(last_startid,20,1)
    pageSeq = last_startid
    if jsonUrlsStr:
       jsonUrlObj = json.loads(jsonUrlsStr)

       if (jsonUrlObj["result"]["code"] == "OK"):
            reccount     = jsonUrlObj["data"]["data_recode_count"]
            #rec_count    = int(reccount)
            record_count = string.atoi(reccount);

            if(record_count > 0):
                #last_startid += record_count
                recordlist = jsonUrlObj["data"]["data_record_list"]
                for record in recordlist:
                    #print record["link_url"],'\n'
                    pageContent = getPageContent(record["link_url"])
                    title = record["title"]
                    pageContent  = getBodyWithoutScript(pageContent)

                    pageContent  = getImgWithSrc(pageContent,pageSeq)

                    pageContent  = getWxImgInPage(pageContent,pageSeq,'data-src')
                    pageContent  = getWxImgInPage(pageContent,pageSeq,'data-backsrc')

                    #print pageContent
                    #root_tag = wxsoup.new_tag('div')
                    pageContent = getTextAndImg(pageContent)
                    #print pageContent

                    pageSeq += 1

                    mkdir(title)
                    savePage(title,pageContent)

                    login("tangzhen","123456")
                    postarticle(title,pageContent)
                    last_startid += 1

    return last_startid
    
def save_last_startid(last_startid):    
    fileName = 'laststartid.txt'
    f = open(fileName,"w+")
    print u"Saving page", last_startid
    strlast_startid = str(last_startid)
    f.write(strlast_startid)

def read_last_startid():    
    fileName = 'laststartid.txt'
    if( os.path.exists(fileName) ):
       f = open(fileName)
       line = f.readline()  
       if line:
          last_startid = string.atoi(line)
       else:
          last_startid = 0
       f.close()
    else:
       last_startid = 0
       
    return last_startid
     
if __name__ == '__main__':
    print u"你好世界" 
    last_startid = read_last_startid()
    print last_startid
    #while True:
    #    print u"Sleeping"
    #    time.sleep(3*60)
    #     
    last_startid = loop_body(last_startid)
    save_last_startid(last_startid)
