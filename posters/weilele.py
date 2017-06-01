#coding=utf-8

import sys
import urllib
import urllib2
# import cookielib
from helper.tools import *
import json
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods import posts
from wordpress_xmlrpc.methods import taxonomies
from wordpress_xmlrpc import WordPressTerm
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers


reload(sys)
sys.setdefaultencoding('utf8')
sys.setrecursionlimit(2000)


class WPPoster:
    wp_url      = "http://www.microlele.com/dev/wp-json/wp/v2/posts"
    wp_url_tags = "http://www.microlele.com/dev/wp-json/wp/v2/tags"
    username    = "admin"
    password    = "Tjjtds@1"
    
    def __init__(self):
       pass 

    def post2wp(self,title,content,fImgId):
        #ready_cate_id = "11"
        wp_data = {}
        wp_headers = {}
        #old_tags = {}

        # todo 先获取所有的 old tags
        #res_old_tags = Crawl_helper_tools_url.http_auth_handle_get_tag(Wpposter.wp_url_tags,wp_data)
        #if (res_old_tags == "fail"):
        #    print('获取标签失败')
        #    sys.exit()

        #decode_res_tags = json.loads(res_old_tags)
        #for res_tag in decode_res_tags:
        #    old_tags[res_tag['name']] = res_tag['id']
        #print('已经存在的标签列表：')
        #print(old_tags)


        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0','Referer' : 'http:www.microlele.com'}


        try:

            page_content = content;
            
            #wp_data['featured_media'] = ''
            wp_data['status']  = "draft"
            wp_data['title']   =  title 
            wp_data['content'] = page_content
            wp_data['author']  = 1
            #wp_data['categories'] ='69,84,57' 
            wp_data['categories'] ='88' # 小助手
            if fImgId:
                wp_data['featured_media'] = fImgId
            #wp_data['slug'] = "test"
            #wp_data['categories[0]'] = ready_cate_id

            #for tag_i in range(len(page_tags)):
             #   print(page_tags[tag_i])
              #  wp_data["tags["+str(tag_i)+"]"] = old_tags[page_tags[tag_i].decode('utf-8')]
            
         
            res = Crawl_helper_tools_url.http_auth(
                                                   WPPoster.username,
                                                   WPPoster.password,
                                                   WPPoster.wp_url,
                                                   wp_data,
                                                   wp_headers)

            if (res == "fail"):
                print u"添加失败"
            # sys.exit()

        except Exception , e:
            print u'except 某篇文章出错....',e

    def getImg2Local(self,imgUrl,pageSeq,saveDir):

        imgName  = imgUrl[imgUrl.rfind('/')+1:]
        imgName  = unicode(pageSeq) + imgName
        imgPath  = saveDir + imgName 
        print imgName,imgPath

        try:
            imgReq = urllib2.Request(imgUrl) 
            res = urllib2.urlopen(imgReq)

            f = open(imgPath,'wb') 
            f.write(res.read()) 
            f.close() 
        except Exception , e:
            print e
            return  None
        return {'filePath':imgPath,
                'imgName':imgName}
 

    def media2wp(self,imgUrl, pageSeq,saveDir):
        wp_data = {}
        wp_headers = {}
        register_openers()

        media = None 

        localImg = self.getImg2Local(imgUrl,pageSeq,saveDir)
        if localImg :
            wp_data, wp_headers = multipart_encode({"file": open(localImg['filePath'], "rb")})
            print wp_headers,'data:', wp_data
            try:
                
                #wp_data['file']  = filepath 
                #wp_headers['Content-Disposition'] = 'attachment;filename=Selection_082.png' 
                #wp_headers['Content-Type'] = 'img/png'
            
                res = Crawl_helper_tools_url.http_auth_media(
                                                       WPPoster.username,
                                                       WPPoster.password,
                                                       'http://www.microlele.com/dev/wp-json/wp/v2/media',
                                                       wp_data,
                                                       wp_headers)

                if (res == "fail"):
                    print u"添加失败"
                else:
                    media = res
                    print res
            

                # sys.exit()

            except Exception , e:
                print u'except 某篇文章出错....',e
            return media
             
class WPRpcPoster:
    wp_url      = "http://www.microlele.com/dev/wp-json/wp/v2/posts"
    wp_url_tags = "http://www.microlele.com/dev/wp-json/wp/v2/tags"
    username    = 'Admin'
    password    = 'Tjjtds@1'
    wp_rpc_url  = 'http://www.microlele.com/dev/xmlrpc.php' 

    def __init__(self,rpcurl,username,password):
        self.wp = Client(rpcurl,username,password)

    def post2wp(title,content):
        post = WordPressPost()
        post.title = title
        post.content = content
        post.post_status = 'draft'

        post.id = self.wp.call(posts.NewPost(post))
        print post.id


if __name__ == "__main__":
    #wpposter = WPRpcPoster(WPRpcPoster.wp_rpc_url, WPRpcPoster.username, WPRpcPoster.password)
    wpposter = WPPoster() 
    #wpposter.post2wp(u'你好微乐乐', u'我的好朋友')
    #wpposter.media2wp(u'/home/ruixj/Pictures/Selection_082.png')
    #imgInfo = wpposter.getImg2Local(u'http://pic-app.lelianyanglao.com/2/src2.jpg', 1,u'/home/ruixj/Pictures/')
    #if imgInfo:
    #    print imgInfo['filePath'],imgInfo['imgName']

    imgInfoJson = wpposter.media2wp(u'http://pic-app.lelianyanglao.com/2/src2.jpg', 1,u'./')#u'/home/ruixj/Pictures/')
    jsonUrlObj = json.loads(imgInfoJson)
    print jsonUrlObj['id']
    wpposter.post2wp(u'你好微乐乐', u'我的好朋友',jsonUrlObj['id'])
    #print jsonUrlObj

