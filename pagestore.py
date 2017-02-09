# -*- coding: utf-8 -*-
import urllib
import urllib2
import cookielib
import json
import string
 
import os
#import md5
import hashlib
from html2ubb import *
import bs4
from bs4 import BeautifulSoup
from putimg2alioss import * 
from extractor import *
from strutil import *
from commonlog import  *
import time


FIREFOX  = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
FIREFOX2 = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' 
    
class lelianStore:
    APPKEY   = "04a13318bc680b9e4da7bba876224a95"
    
    @staticmethod
    def getsign(appkey,apiname):
        src = apiname+appkey
        m1  = hashlib.md5()
        m1.update(src)
        return m1.hexdigest()
    
    @staticmethod
    def login(loginName,loginPwd):
        filename = 'cookie.txt'
        cookie = cookielib.MozillaCookieJar(filename)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        postdata = urllib.urlencode({
                    'user_name':loginName,
                    'password':loginPwd
                })
    
        signkey = lelianStore.getsign(lelianStore.APPKEY,'account')
        loginUrl = 'http://wc.lelianyanglao.com/api/account/login_process/?mobile_sign='+signkey
        #print loginUrl
        
        #send the request to the url
        req = urllib2.Request(loginUrl,postdata)
        req.add_header('User-agent',FIREFOX)
        #result = opener.open(loginUrl,postdata)
        result = opener.open(req)
        
        cookie.save(ignore_discard=True, ignore_expires=True)
        
        loginres = result.read()
        return loginres 
    
    @staticmethod
    def postarticle(title,content):
        cookie = cookielib.MozillaCookieJar()
        cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
    
        #title   = urllib.quote(title)
        title    = title.encode('utf-8')
     
        #content = Html2UBB(content)
        #content = urllib.quote(content)
        content = content.encode('utf-8')
    
        values = {'title':title,
                  'message':content,
                  'category_id':1
                 }
    
        data    = urllib.urlencode(values)
        
        signkey = lelianStore.getsign(lelianStore.APPKEY,'publish')
        publishUrl = 'http://wc.lelianyanglao.com/api/publish/publish_article/?mobile_sign='+signkey
        
        req = urllib2.Request(publishUrl,data)
        req.add_header('User-agent',FIREFOX)
    
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        response = opener.open(req)
        res =  response.read()
        return res

class FileStoreUtil:
    @staticmethod
    def mkdir(path):
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            #print u"creating folder",path
            os.makedirs(path)
            return True 
        else:
            #print "folder ",path," already exists"
            return False
    
    @staticmethod
    def savePage(name,content):
        fileName = name + "/" + name + ".html"
        f = open(fileName,"w+")
        #print u"Saving page", name
        LelianLogger.log('main',logging.INFO,u"\nSaving page: %s",name)
        content = content.encode('utf-8')
        f.write(content)
        
class storeInterface(object):
    def __init__(self):
        pass
    
    def store(self,title,content):
        pass
    
    
class Store2Lelian(storeInterface):
    def __init__(self):
        pass
    
    def store(self,title,content):
        lelianStore.login("乐莲养老","123456")
        lelianStore.postarticle(title,content)
    
class Store2File(storeInterface):
    def __init__(self):
        pass
    
    def store(self,title,content):
        FileStoreUtil.mkdir(title)
        FileStoreUtil.savePage(title,content)

    