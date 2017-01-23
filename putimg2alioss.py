# -*- coding: utf-8 -*-

import oss2
import requests
from itertools import islice
import re
import time

accessKeyId     = "LTAIno40jE5rgKYu";
accessKeySecret = "PR7oD85FzxzeqZjuM3LTG3iopgLqKj";

endpoint = "http://oss-cn-beijing.aliyuncs.com";
bucketname = "lelia-app";
bindroot   = "http://pic-app.lelianyanglao.com/"
def storeImg2AliOss(url,remotename):
    resurl = ''
    try:
        imgres = requests.get(url)
        if(imgres.status_code == requests.codes.ok):
            auth = oss2.Auth(accessKeyId,accessKeySecret)
            bucket = oss2.Bucket(auth,endpoint,bucketname)
            bucket.put_object(remotename,imgres.content)
            resurl = bindroot 
            resurl += remotename
    except Exception:
       print 'invalid URL ', url 
    return resurl

def listImgInOss():
    auth = oss2.Auth(accessKeyId,accessKeySecret)
    bucket = oss2.Bucket(auth,endpoint,bucketname)
    print bucket.get_bucket_location().location
    for b in islice(oss2.ObjectIterator(bucket), 10):
        print(b.key)
        print b.size
        
def getImgExt(url):
    #print url 
    imgFmtReg = re.compile(r'wx_fmt=(.+)')
    #mobj= imgFmtReg.findall(url)
    mobj= imgFmtReg.search(url)
    if mobj:
        #find return match list
        #print mobj[0] 
        return mobj.group(1)
    else:
        return 'jpg'

def checkUrlWithHttp(url):
    if re.match(r'^https?:/{2}\w.+$', url):  
       return True 
    else:  
       return False 

def getPageUrlBaseUri(pageUrl):
    urlpattern = re.compile(r'(https?://)([-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])')
    match = urlpattern.match(pageUrl)
    if match:
        protocol = match.group(1)
        baseUri = match.group(2)
        pathlist = baseUri.split('/')
        listlen  = len(pathlist)        
        if(listlen > 1):
            pathlist = pathlist[:listlen-1] 
        else:
            pathlist = [baseUri]

        pathlist = '/'.join(pathlist)
        baseUri  = protocol
        baseUri  += pathlist
        return baseUri
    else:
        none

def getImgName(pageseq,imgtype,imgseq,imgext):
    #datestr = time.strftime('%Y%m%d',time.localtime(time.time()))
    namelist = [str(pageseq),'/',imgtype,str(imgseq),'.',imgext]
    imgName = ''.join(namelist)
    return imgName
    
if __name__ == '__main__' :
    url = 'http://mmbiz.qpic.cn/mmbiz_jpg/vibkMYdLY6zm63wficQJGJ44PXPHjJ21l55Kk8WpoiaAVa0cCq7BqW5SpdlqZueN1k0VB8IdicPpT6picofqFiasG2JA/0?wx_fmt=jpeg';
    #storeImg2AliOss(url,'1/wx_1.jpeg')
    #listImgInOss()

    #getImgExt(url)

    #datestr = time.strftime('%Y%m%d',time.localtime(time.time()))
    #print datestr

    #print getImgName('wx',1,'jpeg')
    
    getPageUrlBaseUri(url)

    url = 'http://mmbiz.qpic.cn'
    getPageUrlBaseUri(url)
    url = 'http://mmbiz.qpic.cn/'
    getPageUrlBaseUri(url)
    

