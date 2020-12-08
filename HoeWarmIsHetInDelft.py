from html.parser import HTMLParser

import urllib.request
import re

SITE_URL = "https://www.weerindelft.nl"
temp = None
iframe = {'src': None}

class TempParser(HTMLParser):
    '''Custom Temperature Parser class'''

    def __init__(self):
        super().__init__()
        self.reset()
        #flag to enable data gathering
        self.collect_data = False
        self.temp = None
    
    def handle_starttag(self, tag, attrs):
        # Parse only ifrm_3 tag for src script url with temp 
        if tag == "iframe":
            for name, value in attrs:
                if name == "name" and value == "ifrm_3":
                    convert(attrs, iframe)
                    break

        # Parse only span tag with id == 'ajaxtemp' 
        if tag == "span":
           for name, value in attrs:
               if name == "id" and value == "ajaxtemp" :
                   self.collect_data = True
                   break

    def handle_data(self, data):
        #Collect temp data and parse/clean it
        if self.collect_data:
            self.collect_data = False
            self.temp = make_temp_data(data)

def make_html_response(site_url):
    '''returns html code from a url'''
    url = urllib.request.urlopen(site_url)
    html = url.read().decode()
    url.close()
    return html

def make_temp_data(data):
    '''returns temperature from full span text'''
    temp_data = re.search(r'(\-*\d+\.+\d+)', data, re.M|re.I)
    if temp_data:
        temp_data = round(float(temp_data.group()))
    return temp_data

def convert(tup, di):
    '''convert list of tuples to dict'''
    for a, b in tup: 
        di[a] = b
    return di

if __name__ == "__main__":

    p = TempParser()
    p.feed(make_html_response(SITE_URL))

    if iframe['src'] is not None:
        p.feed(make_html_response(iframe['src']))
        if p.temp is not None:
            print(p.temp, 'degrees Celsius')
        else:
            print('Error: Parsing temperature. Please adapt make_temp_data function and/or TempParser class.')
    else:
        print('Error: Page structure changed. Please adapt class TempParser.')