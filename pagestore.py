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

class Store2Weilele(storeInterface):
    @staticmethod
    def http_auth_post(username, password, url, data = {}, headers = {}):
        auth = base64.b64encode(username+ ':'+ password)
        headers["Authorization"] = "Basic "+ auth
 
        # data - dict
        data = urllib.urlencode(data)
        req = urllib2.Request(url, data, headers)
        try:
            response = urllib2.urlopen(req,timeout=5)
        except socket.timeout:
            LelianLogger.log('main',logging.ERROR,u"\n time out")
            return 'fail'
        except Exception , e:
            LelianLogger.log('main',logging.ERROR,u"\n Exception".e)
            return 'fail'
 
        return response.read()

    @staticmethod
    def login(loginName,loginPwd):
        filename = 'cookie.txt'
        cookie = cookielib.MozillaCookieJar(filename)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        postdata = urllib.urlencode({
                    'log':loginName,
                    'pwd':loginPwd
                })
    
        signkey = lelianStore.getsign(lelianStore.APPKEY,'account')
        loginUrl = 'http://www.microlele.com/dev/wp-login.php'
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
 
    def __init__(self):
        pass

    def store(self,title,content):
        wp_url      = "http://www.microlele.com/dev/wp-json/wp/v2/posts"
        wp_url_tags = "http://www.microlele.com/dev/wp-json/wp/v2/tags"
        username    = "Admin" 
        password    = "Tjjtds@1"

        try:
            page_content = content;
            title        = title;
         
            wp_data['status']  = "draft"
            wp_data['title']   = title 
            wp_data['content'] = page_content
            wp_data['author']  = 1
            #wp_data['slug'] = "test"
            #wp_data['categories[0]'] = ready_cate_id
         
            #for tag_i in range(len(page_tags)):
            #   print(page_tags[tag_i])
            #   wp_data["tags["+str(tag_i)+"]"] = old_tags[page_tags[tag_i].decode('utf-8')]
            res = Store2Weilele.http_auth_post(username,password,wp_url,wp_data,wp_headers)
         
            if (res == "fail"):
                LelianLogger.log('main',logging.ERROR,u"\nSaving page to weilele failed.")
            else:
                LelianLogger.log('main',logging.INFO,u"\nSaving page to weilele successfully.")
        except Exception , e:
            LelianLogger.log('main',logging.ERROR,u"\nSaving page to weilele failed. Exception:".e)


    
