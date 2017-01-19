import bs4
from bs4 import BeautifulSoup
html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>
<div>
  teste
  <p> test2 </p>
  test3
</div>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<div>
   <img src="lcoahot"/>
   <p> test4</p>
   ssss
   <!--sxxxx---->
<p class="story">...</p>
</body>
"""
def processChildren(elem,news,newsoup):
    for child in elem.contents:
        if isinstance(child,bs4.element.Tag):
            if (child.name == 'p'):
                #append this element to new content                                                                                                                                                          
                #newp = newsoup.new_tag('p')
                #for elem in child.contents :
                #    newp.append(elem)
                #print child.name
                tag = child.extract()
                #print tag
                #print child 
                news.append(tag)
            elif(child.name == 'img'):
                tag = child.extract()
                #print tag
                news.append(tag)
                #print child.name
            else:       
                processChildren(child,news,newsoup)
                     
        elif isinstance(child,bs4.element.NavigableString):
            nstr = newsoup.new_string(child)
            news.append(nstr)
        else:        
           continue 

from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc)
newsoup = BeautifulSoup('')
btagnew = newsoup.new_tag('body')
newsoup.append(btagnew)
btag = soup.body
#print btag.contents
processChildren(btag,btagnew,newsoup)
print newsoup
