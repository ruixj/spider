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
from readability import Readability
from itertools import compress

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
            LelianLogger.log('main',logging.ERROR,u"invalid page")
    
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
            LelianLogger.log('main',logging.INFO,u"img src url: %s",imgurl)
            resurl = storeImg2AliOss(imgurl,imgName)
            LelianLogger.log('main',logging.INFO,u"lelian pic url: %s",resurl)
            #print 'lelian pic url:', resurl
    
            img['src'] = resurl
            style = img.get('style')
            if(style):
                style = strUtil.removeAttrInCss(style,'opacity')
                img['style'] = style
            imgSeq += 1
    
        return unicode(wxpsoup)
    
    @staticmethod
    def getWxImgInPage(page,pageSeq,attr):
        if not page:
            #print u"invalid page"
            LelianLogger.log('main',logging.ERROR,u"invalid page")
    
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
            LelianLogger.log('main',logging.INFO,u"imgurl:%s",imgurl)
            resurl = storeImg2AliOss(imgurl,imgName)
            LelianLogger.log('main',logging.INFO,u"lelianpic url:%s",resurl)
            #print 'lelianpic url:',resurl
    
            img['src'] = resurl
    
            style = img.get('style')
            if(style):
                style = strUtil.removeAttrInCss(style,'opacity')
                img['style'] = style
    
            imgSeq +=1
    
        return unicode(wxpsoup)
    
    @staticmethod
    def getWxIframeInPage(page,pageSeq,attr):
        if not page:
            #print u"invalid page"
            LelianLogger.log('main',logging.ERROR,u"invalid page")
    
        wxpsoup = BeautifulSoup(page)
        #1. find img 
        datasrcImgList = wxpsoup.find_all("iframe",attrs={attr: True})
        imgSeq = 1
        for hiframe in datasrcImgList:
            imgurl = hiframe[attr]
            imgurl = strUtil.removeSpace(imgurl)
    
            imgExt = getImgExt(imgurl)
            imgName = getImgName(pageSeq,attr,imgSeq,imgExt)
    
            if(not checkUrlWithHttp(imgurl)):
                if imgurl:
                    imgurl = "http:" + imgurl
                else:
                    continue
                
            #print 'imgurl:',imgurl
            LelianLogger.log('main',logging.INFO,u"imgurl:%s",imgurl)
            resurl = imgurl;
            LelianLogger.log('main',logging.INFO,u"lelianpic url:%s",resurl)
            #print 'lelianpic url:',resurl
    
            hiframe['src'] = resurl
    
            style = hiframe.get('style')
            if(style):
                style = strUtil.removeAttrInCss(style,'opacity')
                hiframe['style'] = style
    
            imgSeq +=1
    
        return unicode(wxpsoup)
        
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
        LelianLogger.log('main',logging.INFO,u"page baseUri: %s",kwargs['pageBaseUri'])
        if kwargs['pageBaseUri']:
            pageContent  = ImgUtil.getImgWithSrc(kwargs['pageContent'],kwargs['pageSeq'],kwargs['pageBaseUri'])
 
            pageContent  = ImgUtil.getWxImgInPage(pageContent,kwargs['pageSeq'],'data-src')
 
            pageContent  = ImgUtil.getWxImgInPage(pageContent,kwargs['pageSeq'],'data-backsrc')
            
            pageContent  = ImgUtil.getWxIframeInPage(pageContent,kwargs['pageSeq'],'data-src')
            
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
            
        styles = wxsoup.find_all("style")
        for style in styles:
            style.decompose()
            
        links = wxsoup.find_all("link")
        for link in links:
            link.decompose()            
            
        content = unicode(wxsoup.body)
        return content 
    
class TitleProcessor(ProcessorInterface):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''     
    def process(self,**kwargs):  
        wxsoup = BeautifulSoup(kwargs['pageContent'])
        name = wxsoup.find('title')
        return name.string

class FirstImgProcessor(ProcessorInterface):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''     
    def process(self,**kwargs):  
        wxsoup = BeautifulSoup(kwargs['pageContent'])
        #print kwargs['pageContent']
        #firstImg= wxsoup.find("img",attrs={'src': True})
        Imglist= wxsoup.find_all("img",attrs={'src': True})
        ImgNum = len(Imglist)
        if ImgNum == 1:
          imgurl = Imglist[0]['src']
        elif ImgNum > 1:
          imgurl = Imglist[1]['src']
        else:
            imgurl = None 
        #print imgurl 
        #print firstImg
        #if firstImg:
        #    imgurl = firstImg['src']
        #name = soup.find('img')

        return imgurl 
    
    
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
        
        #return unicode(newsoup)
        return newsoup.prettify()

class ReadProcessor(ProcessorInterface):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
    def process(self,**kwargs):
        pageContent = kwargs['pageContent']
        url         = kwargs['pageBaseUri']
        
        readability = Readability(pageContent,url)

        return readability.content
    
class FormatProcessor(ProcessorInterface):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
    def process(self,**kwargs):
        pageContent = kwargs['pageContent']
        ContentLines = pageContent.splitlines()
        compressedContent = ''
        for cl in ContentLines:
            if cl[-1] == u'>':
                compressedContent += cl
            else:
                compressedContent += cl
                compressedContent += u'\n'
        return compressedContent
                

         
