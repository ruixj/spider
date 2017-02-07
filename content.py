# -*- coding: utf-8 -*-
'''
Created on 2017-1-28

@author: xrui
'''
import urllib
import urllib2
import cookielib
import json
import string
from commonlog import LelianLogger
import logging
from qt4wkrender import QtWKPageRender

FIREFOX2 = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
class ContentProvider(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
    def getContent(self,src):   
        pass
    
class UrlContentProvider(ContentProvider):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        
    def getContent(self,url):   
        headersL = {'User-Agent':FIREFOX2}
        try:    
            req = urllib2.Request(url,headers=headersL)
            response = urllib2.urlopen(req)
            page = response.read()
            return page 
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                #print u"Fail to get page from ",url
                LelianLogger.log('main',logging.ERROR,u"\nFail to get page from %s",url)
                return None
            
class FileContentProvider(ContentProvider):    
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        
    def getContent(self,filePath):   
        f = open(filePath)
        fileContent = f.read()
        return fileContent           


class DynamicContentProvider(ContentProvider):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
    def getContent(self,url):
        r = QtWKPageRender(url)
        result = r.frame.toHtml()
        content = str(result.toUtf8())
        return content

