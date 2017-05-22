from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo

wp = Client('http://www.microlele.com/dev/xmlrpc.php', 'Admin', 'Tjjtds@1')
wp.call(GetPosts())
 
