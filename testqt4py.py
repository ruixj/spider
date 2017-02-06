import sys  
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *  
from lxml import html 

class Render(QWebPage):  
  def __init__(self, url):  
    self.app = QApplication(sys.argv)  
    QWebPage.__init__(self)  
    self.settings().setAttribute(QWebSettings.LocalStorageEnabled,True)
    self.loadFinished.connect(self._loadFinished)  
    self.mainFrame().load(QUrl(url))  
    self.app.exec_()  
  
  def _loadFinished(self, result):  
    self.frame = self.mainFrame()  
    self.app.quit() 

if __name__ == '__main__' :
    #url = 'http://pycoders.com/archive/'  
    url = 'https://36kr.com/p/5061197.html'
    #QWebSettings.globalSettings().setAttribute(QWebSettings.LocalStorageEnabled,True)
    #This does the magic.Loads everything
    r = Render(url)  
    #result is a QString.
    result = r.frame.toHtml()
    #print result.encode('utf-8')
    #result = r.toHtml()
    #print r
    #QString should be converted to string before processed by lxml
    formatted_result = str(result.toUtf8())
    print formatted_result

    #Next build lxml tree from formatted_result
    #tree = html.fromstring(formatted_result)

    #Now using correct Xpath we are fetching URL of archives
    #archive_links = tree.xpath('//divass="campaign"]/a/@href')
    #print archive_links
