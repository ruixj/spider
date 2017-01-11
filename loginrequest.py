import urllib
import urllib2
import cookielib
import json

def login():
    filename = 'cookie.txt'
    cookie = cookielib.MozillaCookieJar(filename)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    postdata = urllib.urlencode({
                'user_name':'ustb_ruixj@163.com',
                'password':'ruiking1'
            })
    loginUrl = 'http://wecenter.dev.hihwei.com/api/account/login_process/'
    result = opener.open(loginUrl,postdata)
    cookie.save(ignore_discard=True, ignore_expires=True)
    #print result.read()
    return result

def postarticle():
    cookie = cookielib.MozillaCookieJar()
    cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)

    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

    values = {'username':'cqc',
              'password':'xxx'
             }
    headers = {'User-Agent':user_agent}
    data    = urllib.urlencode(values)
    
    req = urllib2.Request('http://wecenter.dev.hihwei.com/api/publish/publish_article/',data,headers)

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    response = opener.open(req)
    #print response.read() 
    return response

def geturls(start_id,page_size,page_num):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    values = {'start_id':start_id,
              'page_size':page_size,
              'p':page_num
             }
    headers = {'User-Agent':user_agent}
    data    = urllib.urlencode(values)
    
    req = urllib2.Request('http://m.lelianyanglao.com/index.php?m=api&a=get_splider_list',data,headers)
    response = urllib2.urlopen(req)
    #print response.read()
    return response

def getPageContent(url):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    values = {
             }
    headers = {'User-Agent':user_agent}
    data    = urllib.urlencode(values)
    
    req = urllib2.Request(url,data,headers)
    response = urllib2.urlopen(req)
    #print response.read()
    return response

   

if __name__ == '__main__':
    #login()
    res = geturls(0,20,1)
    print res.read()
