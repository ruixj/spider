#coding=utf-8
import urllib
import re

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    print html
    return html

def getImg(html):
    reg = r'src="(.+?\.jpg)" pic_ext'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    x = 0
    for imgurl in imglist:
        urllib.urlretrieve(imgurl,'%s.jpg' % x)
        x+=1

if __name__ == '__main__':
    #html = getHtml("http://tieba.baidu.com/p/2460150866")
    html = getHtml("http://mp.weixin.qq.com/s/FKFWdjMpNZ60dWMyf8WF3A")
    print getImg(html)
