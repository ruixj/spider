import urllib2

def readurl(url)
    reponse = urllib2.urlopen(url)
    print reponse.read()

#response = urllib2.urlopen("http://www.baidu.com")
#print response.read()



