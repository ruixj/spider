'''
Created on 2017-1-19

@author: xrui
'''
import bs4
from bs4 import BeautifulSoup
from bs4 import Comment


def copyElement(elem,news,newsoup):
    elemtxt = elem.prettify()
    soup = BeautifulSoup(elemtxt)
    roottag = soup.contents[0].extract()
    news.append(roottag)
    
def processChildren(elem,news,newsoup):
    for child in elem.contents:
        if isinstance(child,bs4.element.Tag):
            if (child.name == 'p'):
                #append this element to new content                                                                                                                                                          
                #newp = newsoup.new_tag('p')
                #for elem in child.contents :
                #    newp.append(elem)
                #print child.name
                #tag = child.extract()
                #print tag
                #print child 
                copyElement(child,news,newsoup)
            elif(child.name == 'img'):
                #tag = child.extract()
                #print tag
                #news.append(tag)
                #print child.name
                copyElement(child,news,newsoup)
            else:       
                processChildren(child,news,newsoup)
                     
        elif isinstance(child,bs4.element.NavigableString):
            if isinstance(child,bs4.element.Comment):
                nstr = newsoup.new_string(child,Comment)
                news.append(nstr)
                #pass
            else:
                nstr = newsoup.new_string(child)
                news.append(nstr)
        else:        
           continue 

if __name__ == '__main__':
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
    soup = BeautifulSoup(html_doc)
    newsoup = BeautifulSoup('')
    btagnew = newsoup.new_tag('body')
    newsoup.append(btagnew)
    btag = soup.body
    #print btag.contents
    processChildren(btag,btagnew,newsoup)
    print newsoup
