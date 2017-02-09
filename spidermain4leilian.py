# -*- coding: UTF-8 -*-
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
from  content import *
from  processor import *

from pagestore import *
from ghostcontent import DynamicContentProvider

FIREFOX  = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'

class URLMainProcessor:
    def __init__(self):
        #self.contentProvider = UrlContentProvider()
        self.contentProvider = DynamicContentProvider()
        self.scriptProcessor = ScriptProcessor()
        self.imgProcessor = ImgProcessor()
        self.rdbProcessor = ReadProcessor()
    def geturls(self,start_id,page_size,page_num):
     
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
                #print u"unable to get the urls"
                LelianLogger.log('main',logging.ERROR,u"unable to get the urls")
                return None
            
    def loop_body(self,last_startid):
        jsonUrlsStr= self.geturls(last_startid,20,1)
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
                        title = record["title"]
                        
                        LelianLogger.log('main',logging.INFO,u"processing : %s，page url: %s",title,record["link_url"])
                        #title = title.encode('utf-8')
                        #print '\nprocessing ',title,'\n','page url:',record["link_url"]

                        pageContent = self.contentProvider.getContent(record["link_url"])
                        #pageContent = getPageContent(record["link_url"])
                        if pageContent:
    
                            
                            params = {'pageContent':pageContent}
                            pageContent = self.scriptProcessor.process(**params)
                            
                            pageBaseUri  = getPageUrlBaseUri(record["link_url"])
                            #print "page baseUri:", pageBaseUri
                            LelianLogger.log('main',logging.INFO,u"page baseUri: %s",pageBaseUri)
                            if pageBaseUri:
                                
                                params = {'pageContent':pageContent,
                                          'pageSeq':pageSeq,
                                          'pageBaseUri':pageBaseUri}
                                pageContent  = self.imgProcessor.process(**params)
    
                                params = {'pageContent':pageContent,
                                          'pageBaseUri':pageBaseUri}
                                txtImgProcessor = TxtImgProcessor()
                                pageContent = txtImgProcessor.process(**params)
                                
                                pageContent = pageContent.replace(u'\r',u'').replace(u'\n',u'')
                                
                                #pageContent  = self.rdbProcessor.process(**params)
                                #print pageContent
                                #pageContent  = Html2UBB(pageContent)
                                #print pageContent
                                #mkdir(title)
                                #savePage(title,pageContent)
                                #store = Store2File()
                                store = Store2Lelian()
                                
                                store.store(title, pageContent) 
    
                                #login("tangzhen","123456")
                                #postarticle(title,pageContent)
    
                        self.save_last_startid(last_startid)
                        pageSeq += 1
                        last_startid += 1
    
        return last_startid
        
    def save_last_startid(self,last_startid):    
        fileName = 'laststartid.txt'
        f = open(fileName,"w+")
        
        LelianLogger.log('main',logging.INFO,u"Saving page : %s",last_startid)
        #print u"Saving page", last_startid
        strlast_startid = str(last_startid)
        f.write(strlast_startid)
    
    def read_last_startid(self):    
        fileName = 'laststartid.txt'
        if( os.path.exists(fileName) ):
            f = open(fileName)
            line = f.readline()  
            if line:
                last_startid = string.atoi(line)
            else:
                last_startid = 1
            f.close()
        else:
            last_startid = 1
           
        return last_startid
    
    def main(self):
        last_startid = self.read_last_startid()
        LelianLogger.log('main',logging.INFO,u"starting last_startid : %s",last_startid)
        #last_startid +=1
        while True:
            last_startid_new = self.loop_body(last_startid)
            self.save_last_startid(last_startid_new)
            if(last_startid_new  == last_startid ):
                LelianLogger.log('main',logging.INFO,u"Sleeping")
                time.sleep(3*60)
            else:
                last_startid = last_startid_new
            LelianLogger.log('main',logging.INFO,u"last_startid : %s",last_startid)


    
if __name__ == '__main__':
    LelianLogger.configLog('logging.conf')
    mainProcessor = URLMainProcessor()
    mainProcessor.main()
