# -*- coding: UTF-8 -*-
import urllib2

def sendReq(url):
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    print response.read()

if __name__ == "__main__" :
    sendReq("http://www.baidu.com")




