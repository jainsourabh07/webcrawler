from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib import parse

# Creating a class called LinkParser that inherits some
# methods from HTMLParser
# which is why it is passed into the definition
class LinkParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        # looking for the begining of a link. 
        if tag  == 'img' or tag == 'a':
            for (key, value) in attrs:
                if key == 'src' or key == 'href':
                    # Grabbing the new URL and adding the
                    # base URL to it. 
                    # Combine a relative URL with the base URL to create
                    # an absolute URL like:
                    newUrl = parse.urljoin(self.baseUrl, value)
                    # Add it to our colection of links:
                    if not newUrl.find(self.baseUrl) :
                        self.links = self.links + [newUrl]

    # Function to get all the lnks that crawler() function will call
    def getLinks(self, url):
        self.links = []
        self.baseUrl = url
        response = urlopen(url)
        # Resticting to look only HTML files.
        if response.getheader('Content-Type')=='text/html':
            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")
            self.feed(htmlString)
            return htmlString, self.links
        else:
            return "",[]

# crawler takes in an URL 
# and the number of pages to search through before giving up
def crawler(url, maxPages):  
    pagesToVisit = [url]
    numberVisited = 0
    # The main loop. Create a LinkParser and get all the links on the page.
    # In our getLinks function we return the web page
    # and we return a set of links from that web page
    # (this is useful for where to go next)
    while numberVisited < maxPages and pagesToVisit != []:
        numberVisited = numberVisited +1
        # Start from the beginning of our collection of pages to visit:
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]
        try:
            print(numberVisited, ":", url)
            parser = LinkParser()
            data, links = parser.getLinks(url)
            # Add the pages that we visited to the end of our collection
            # of pages to visit:
            pagesToVisit = pagesToVisit + links
        except:
            print(" **Failed!**")
