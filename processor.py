# -*- coding: UTF-8 -*-
'''
Created on 2017-1-28

@author: xrui
'''
import bs4
from bs4 import BeautifulSoup
from putimg2alioss import *
from commonlog import LelianLogger
import logging
from strutil import *
from extractor import *
class ProcessorInterface(object):
    '''
    classdocs
    '''
    def __init__(self, params):
        '''
        Constructor
        '''
    def process(self,**kwargs):  
        pass

class ImgUtil:
    @staticmethod
    def getImgWithSrc(page,pageSeq,pageBaseUri):
        if not page:
            #print u"invalid page"
            LelianLogger.log('main',logging.ERROR,u"\ninvalid page")
    
        wxpsoup = BeautifulSoup(page)
        #getTextAndImg(wxpsoup)
        #1. find img 
        datasrcImgList = wxpsoup.find_all("img",attrs={'src': True})
        imgSeq = 1
        for img in datasrcImgList:
            imgurl = img['src']
            imgurl = strUtil.removeSpace(imgurl)
    
            if imgurl == '':
                imgSeq += 1
                continue
    
            #check if only with img name
            #append page url
            if(not checkUrlWithHttp(imgurl)):
                if( imgurl.startswith('//')):
                    imgurl = 'http:' + imgurl
                else:
                    imgurl = pageBaseUri + '/' + imgurl
    
            imgExt = 'jpg'  
            imgName = getImgName(pageSeq,'src',imgSeq,imgExt)
    
            #print 'img src url:', imgurl
            LelianLogger.log('main',logging.INFO,u"\nimg src url: %s",imgurl)
            resurl = storeImg2AliOss(imgurl,imgName)
            LelianLogger.log('main',logging.INFO,u"\nlelian pic url: %s",resurl)
            #print 'lelian pic url:', resurl
    
            img['src'] = resurl
            style = img.get('style')
            if(style):
                style = strUtil.removeAttrInCss(style,'opacity')
                img['style'] = style
            imgSeq += 1
    
        return wxpsoup.prettify()
    
    @staticmethod
    def getWxImgInPage(page,pageSeq,attr):
        if not page:
            #print u"invalid page"
            LelianLogger.log('main',logging.ERROR,u"\ninvalid page")
    
        wxpsoup = BeautifulSoup(page)
        #1. find img 
        datasrcImgList = wxpsoup.find_all("img",attrs={attr: True})
        imgSeq = 1
        for img in datasrcImgList:
            imgurl = img[attr]
            imgurl = strUtil.removeSpace(imgurl)
    
            imgExt = getImgExt(imgurl)
            imgName = getImgName(pageSeq,attr,imgSeq,imgExt)
    
            if(not checkUrlWithHttp(imgurl)):
                if imgurl:
                    imgurl = "http:" + imgurl
                else:
                    continue
                
            #print 'imgurl:',imgurl
            LelianLogger.log('main',logging.INFO,u"\nimgurl:%s",imgurl)
            resurl = storeImg2AliOss(imgurl,imgName)
            LelianLogger.log('main',logging.INFO,u"\nlelianpic url:%s",resurl)
            #print 'lelianpic url:',resurl
    
            img['src'] = resurl
    
            style = img.get('style')
            if(style):
                style = strUtil.removeAttrInCss(style,'opacity')
                img['style'] = style
    
            imgSeq +=1
    
        return wxpsoup.prettify()
    
 
        
class ImgProcessor(ProcessorInterface):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''     
    def process(self,**kwargs):      
    #def process(self,pageContent,pageSeq,pageBaseUri):  
        #print "page baseUri:", pageBaseUri
        LelianLogger.log('main',logging.INFO,u"\npage baseUri: %s",kwargs['pageBaseUri'])
        if kwargs['pageBaseUri']:
            pageContent  = ImgUtil.getImgWithSrc(kwargs['pageContent'],kwargs['pageSeq'],kwargs['pageBaseUri'])
            pageContent  = ImgUtil.getWxImgInPage(kwargs['pageContent'],kwargs['pageSeq'],'data-src')
            pageContent  = ImgUtil.getWxImgInPage(kwargs['pageContent'],kwargs['pageSeq'],'data-backsrc')
            
        return pageContent
    
class ScriptProcessor(ProcessorInterface):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''     
    def process(self,**kwargs):  
        wxsoup = BeautifulSoup(kwargs['pageContent'])
    
        scripts= wxsoup.find_all("script")
        for script in scripts:
            script.decompose()
    
        content = str(wxsoup.body)
        return content 
    
class TxtImgProcessor(ProcessorInterface):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''     
    def process(self,**kwargs):  
        wxsoup = BeautifulSoup(kwargs['pageContent'],'html.parser')
        bodyElem = wxsoup.body
        #print bodyElem.prettify()
        #print bodyElem.contents[0]
        #loop through the children
        newsoup = BeautifulSoup('')
        btagnew = newsoup.new_tag('div')
        newsoup.append(btagnew) 
        #processChildren2(bodyElem,btagnew,newsoup)
        processChildren(bodyElem,btagnew,newsoup)