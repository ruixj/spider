# -*- coding: UTF-8 -*-
import re

def Html2UBB(content):
    #以下是将html标签转为ubb标签
    pattern = re.compile( u'<a href=\"([sS]+?)\"[^>]*>([sS]+?)</a>',re.I)
    content = pattern.sub(ur'[url=\1]\2[/url]',content)
    pattern = re.compile( u'<img[^>]+src=\"([^\"]+)\"[^>]*>',re.I)
    content = pattern.sub(ur'[img]\1[/img]',content)
    pattern = re.compile( u'<strong>([sS]+?)</strong>',re.I)
    content = pattern.sub(ur'[b]\1[/b]',content)
    pattern = re.compile( u'<font color=\"([sS]+?)\">([sS]+?)</font>',re.I)
    content = pattern.sub(ur'[\1]\2[/\1]',content)
    pattern = re.compile( u'<[^>]*?>',re.I)
    content = pattern.sub(u'',content)
    #以下是将html转义字符转为普通字符
    content = content.replace(u'<',u'<')
    content = content.replace(u'>',u'>')
    content = content.replace(u'”',u'”')
    content = content.replace(u'“',u'“')
    content = content.replace(u'"',u'"')
    content = content.replace(u'©',u'©')
    content = content.replace(u'®',u'®')
    content = content.replace(u' ',u' ')
    content = content.replace(u'—',u'—')
    content = content.replace(u'–',u'–')
    content = content.replace(u'‹',u'‹')
    content = content.replace(u'›',u'›')
    content = content.replace(u'…',u'…')
    content = content.replace(u'&',u'&')
    return content

if __name__ == '__main__':
    content = u'<html> <p> <img data-ratio="1.732" data-s="300,640" data-src="http://mmbiz.qpic.cn/mmbiz/IiaibG8hibXx5QicHatjEbhOqgUKicz19DmMTIPZ2uucyOpg3QibWPCXQaOYaQ3bBFUVvTYF7CuBSpHoWDH8vpE5HAdA/0?wx_fmt=jpeg" data-type="jpeg" data-w="500" src="http://pic-app.lelianyanglao.com/38/data-src8.jpeg"/></p> </html>'
    Html2UBB(content)
