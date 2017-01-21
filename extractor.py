'''
Created on 2017-1-19

@author: xrui
'''
import bs4
from bs4 import BeautifulSoup
from bs4 import Comment
import re
 
       
def copyPTag(elem,news,newsoup):
    pnewTag = newsoup.new_tag('p')
    news.append(pnewTag)
    processChildren(elem,pnewTag,newsoup)

def copyNonDivTag(elem,news,newsoup):
    pnewTag = newsoup.new_tag(elem.name)
    news.append(pnewTag)
    processChildren2(elem,pnewTag,newsoup)
   
def copyElement(elem,news,newsoup):
    elemtxt = elem.prettify()
    soup = BeautifulSoup(elemtxt,'html.parser')
    roottag = soup.contents[0].extract()
    news.append(roottag)

def astrcmp(str1,str2):
    return str1.lower()==str2.lower()

def processChildren2(elem,news,newsoup):
    for child in elem.contents:
        if isinstance(child,bs4.element.Tag):
            if (astrcmp(child.name,'img')):
                copyElement(child,news,newsoup)
            elif (not (astrcmp(child.name,'div')
                      or astrcmp(child.name,'section'))):
                copyNonDivTag(child,news,newsoup)
            else:
                processChildren2(child,news,newsoup)

        elif isinstance(child,bs4.element.NavigableString):
            if isinstance(child,bs4.element.Comment):
                nstr = newsoup.new_string(child,Comment)
                news.append(nstr)
            else:
                nstr = newsoup.new_string(child)
                news.append(nstr)
        else:
            continue

def processChildren(elem,news,newsoup):
    for child in elem.contents:
        if isinstance(child,bs4.element.Tag):
            style = child['sytle']
            imgFmtReg = re.compile(r'display:none')
            mobj= imgFmtReg.search(url)
            if mobj:
                continue

            if (child.name == 'p'):
                copyPTag(child,news,newsoup)
            elif(astrcmp(child.name, 'img') 
                 or astrcmp(child.name, 'b') 
                 or astrcmp(child.name, 'span')
                 or astrcmp(child.name,'strong')
                 or astrcmp(child.name,'li')
                 or astrcmp(child.name,'ul')
                 ):
            #elif(not astrcmp(child.name,'div')):
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
      <p> <div>test2</div> test21 </p>
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

