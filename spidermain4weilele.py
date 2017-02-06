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
from pip._vendor.requests.packages.urllib3 import filepost

from pagestore import *

FIREFOX  = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'

class URLMainProcessor:
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
                LelianLogger.log('main',logging.ERROR,u"\nunable to get the urls")
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
                        
                        LelianLogger.log('main',logging.INFO,u"\nprocessing : %s，page url: %s",title,record["link_url"])
                        #title = title.encode('utf-8')
                        #print '\nprocessing ',title,'\n','page url:',record["link_url"]
                        contentProvider = UrlContentProvider()
                        pageContent = contentProvider.getContent(record["link_url"])
                        #pageContent = getPageContent(record["link_url"])
                        if pageContent:
    
                            scriptProcessor = ScriptProcessor()
                            params = {'pageContent':pageContent}
                            pageContent = scriptProcessor.process(**params)
                            
                            pageBaseUri  = getPageUrlBaseUri(record["link_url"])
                            #print "page baseUri:", pageBaseUri
                            LelianLogger.log('main',logging.INFO,u"\npage baseUri: %s",pageBaseUri)
                            if pageBaseUri:
                                imgProcessor = ImgProcessor()
                                params = {'pageContent':pageContent,
                                          'pageSeq':pageSeq,
                                          'pageBaseUri':pageBaseUri}
                                pageContent  = imgProcessor.process(**params)
    
                                params = {'pageContent':pageContent}
                                txtImgProcessor = TxtImgProcessor()
                                pageContent = txtImgProcessor.process(**params)
    
                                #mkdir(title)
                                #savePage(title,pageContent)
                                store = Store2File()
                                store.store(title, content) 
    
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
        print last_startid
        #last_startid +=1
        while True:
            last_startid = self.loop_body(last_startid)
            self.save_last_startid(last_startid)
    
            LelianLogger.log('main',logging.INFO,u"Sleeping")
    
            time.sleep(3*60)
             
            print last_startid

class FileMainProcessor:
    def loop_body(self,filePath):
        pageSeq = 1
       
        fileCp = FileContentProvider()
        pageContent = fileCp.getContent(filePath)
        

        if pageContent:
            pageContentWithBody = '<body>' 
            
            pageContentWithBody += pageContent
            
            pageContentWithBody += "</body>"
            
            scriptProcessor = ScriptProcessor()
            params = {'pageContent':pageContentWithBody}
            pageContent = scriptProcessor.process(**params)
   
            imgProcessor = ImgProcessor()
            params = {'pageContent':pageContent,
                      'pageSeq':pageSeq,
                      'pageBaseUri':' '}
            pageContent  = imgProcessor.process(**params)

            print pageContent
            params = {'pageContent':pageContent}
            txtImgProcessor = TxtImgProcessor()
            pageContent = txtImgProcessor.process(**params)

            #mkdir(title)
            #savePage(title,pageContent)

            #login("tangzhen","123456")
            #postarticle(title,pageContent)
            
            store = Store2File()
            store.store('test1', pageContent) 
    
        
    def main(self):
        filePath = 'test.html'
        self.loop_body(filePath)
    
 
    
if __name__ == '__main__':
    LelianLogger.configLog('logging.conf')
    #mainProcessor = URLMainProcessor()
    mainProcessor = FileMainProcessor()
    mainProcessor.main()
