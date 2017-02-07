'''
Created on Feb 7, 2017

@author: ruixj
'''
from ghost import Ghost
from content import ContentProvider

class DynamicContentProvider(ContentProvider):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.gh = None
        self.page = None
        
    def getContent(self,url):
        
        if( self.gh is None):
            self.gh = Ghost()
            self.page, self.page_name = self.gh.create_page()
            
        self.page_resource = self.page.open(url, wait_onload_event=True)
        
        return self.page.content
    
if __name__ == '__main__':
    url = 'https://36kr.com/p/5061197.html'
    gh = Ghost()
    
    # We create a new page
    page, page_name = gh.create_page()
    
    # We load the main page of ebay
    page_resource = page.open(url, wait_onload_event=True)
    print page.content
    url = 'http://www.baidu.com'
    page_resource = page.open(url, wait_onload_event=True)
    print page.content