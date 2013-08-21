"""
Oracle - YouTube Link Converter
~ Toofifty 
"""

import urllib, json

def parselink(url):
    meta_data_link = ('http://www.youtube.com/oembed?url=%s&format=json' % url)
    #print meta_data_link
    
    meta_data_tables = urllib.urlopen(meta_data_link)
    meta_data = json.loads(meta_data_tables.read())
    return (meta_data["author_name"], meta_data["title"])