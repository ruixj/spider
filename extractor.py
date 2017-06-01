# -*- coding: UTF-8 -*-
'''
Created on 2017-1-19
@author: xrui
'''
import bs4
from bs4 import BeautifulSoup
from bs4 import Comment
import re

regexps = {
    'unlikelyCandidates': re.compile("combx|comment|community|disqus|extra|foot|header|menu|"
                                     "remark|rss|shoutbox|sidebar|sponsor|ad-break|agegate|"
                                     "pagination|pager|popup|tweet|twitter",re.I),
    'okMaybeItsACandidate': re.compile("and|article|body|column|main|shadow", re.I),
    'positive': re.compile("article|body|content|entry|hentry|main|page|pagination|post|text|"
                           "blog|story",re.I),
    'negative': re.compile("combx|comment|com|contact|foot|footer|footnote|masthead|media|"
                           "meta|outbrain|promo|related|scroll|shoutbox|sidebar|sponsor|"
                           "shopping|tags|tool|widget", re.I),
    'extraneous': re.compile("print|archive|comment|discuss|e[\-]?mail|share|reply|all|login|"
                             "sign|single",re.I),
    'divToPElements': re.compile("<(a|blockquote|dl|div|img|ol|p|pre|table|ul)",re.I),
    'replaceBrs': re.compile("(<br[^>]*>[ \n\r\t]*){2,}",re.I),
    'replaceFonts': re.compile("<(/?)font[^>]*>",re.I),
    'trim': re.compile("^\s+|\s+$",re.I),
    'normalize': re.compile("\s{2,}",re.I),
    'killBreaks': re.compile("(<br\s*/?>(\s|&nbsp;?)*)+",re.I),
    'videos': re.compile("http://(www\.)?(youtube|vimeo)\.com",re.I),
    'skipFootnoteLink': re.compile("^\s*(\[?[a-z0-9]{1,2}\]?|^|edit|citation needed)\s*$",re.I),
    'nextLink': re.compile("(next|weiter|continue|>([^\|]|$)|»([^\|]|$))",re.I),
    'prevLink': re.compile("(prev|earl|old|new|<|«)",re.I)
}   
       
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
    if not elem :
       return 
    for child in elem.contents:
        if isinstance(child,bs4.element.Tag):
            unlikelyMatchString = child.get('id','')+''.join(child.get('class',''))

            if  regexps['unlikelyCandidates'].search(unlikelyMatchString) and \
                not regexps['okMaybeItsACandidate'].search(unlikelyMatchString) and \
                child.name != 'body':
                continue
            
            style = child.get('style')
            if(style):
                imgFmtReg = re.compile(r'display:none')
                mobj= imgFmtReg.search(style)
                if mobj:
                    continue

            if (child.name == 'p'):
                bHasTxt = False
                for str in  child.stripped_strings:
                    if str != u'':
                        bHasTxt = True
                        break
                imglst = child.find_all('img')
                
                if(bHasTxt or len(imglst) > 0): 
                    copyPTag(child,news,newsoup)
                    
            elif ( astrcmp(child.name,'ul')
                   or astrcmp(child.name,'ol')):
                #check if the child has paragraph
                lilist = child.find_all('li')
                alist = child.find_all('a')
                plist = child.find_all('p')
                
                lilstlen= len(lilist)
                alstlen = len(alist)
                plstlen = len(plist)
                
                strlstlen = 0
                for string in child.stripped_strings:
                    strlstlen += 1 
                
                score = 0;
                if(plstlen < alstlen):
                    score += -1
                elif( plstlen > 0 and plstlen >= alstlen):
                    score += 2
                    
                if(strlstlen > 0):
                    score +=1
                    
                if(alstlen == lilstlen):
                    score += -2
                    
                if(score > 0):
                   copyElement(child,news,newsoup)
                else:
                    continue
                                  
            elif(astrcmp(child.name, 'img') 
                 or astrcmp(child.name, 'b') 
                 or astrcmp(child.name, 'span')
                 or astrcmp(child.name,'strong')
                 or astrcmp(child.name,'li')
                 or astrcmp(child.name,'h1')
                 or astrcmp(child.name,'h2')
                 or astrcmp(child.name,'h3')
                 or astrcmp(child.name,'h4')
                 or astrcmp(child.name,'h5')
                 or astrcmp(child.name,'h6')
                 or astrcmp(child.name,'blockquote')
                 or astrcmp(child.name,'hr')
                 or astrcmp(child.name,'i')
                 or astrcmp(child.name,'del')
                 or astrcmp(child.name,'ins')
                 or astrcmp(child.name,'em')
                 or astrcmp(child.name,'big')
                 or astrcmp(child.name,'small')
                 or astrcmp(child.name,'sub')
                 or astrcmp(child.name,'sup')
                 or astrcmp(child.name,'embed')
                 or astrcmp(child.name,'iframe')
                 or astrcmp(child.name,'br')
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
