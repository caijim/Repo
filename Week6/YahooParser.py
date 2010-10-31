import BeautifulSoup, urllib2,json


class LookupImage():
    image = None
    query = None
    appid = 'AOkWGm7V34HVSRxUwrlQCjNxzBfgVVXQrT4BARjs46M7.cWZSLeGu9UOGEwAPbPIBjehTYA-'
    def __init__(self, query):
        self.query = '+'.join(query.split())
    def lookUp(self):
        url = 'http://search.yahooapis.com/ImageSearchService/V1/imageSearch?appid=%s=&query=%s&results=10&output=json' %(self.appid, self.query)
        page = urllib2.urlopen(url)
        bibJson = json.loads(page.read())
        return bibJson



