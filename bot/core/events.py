import time
import calendar
import urllib
from datetime import datetime
from xml.dom import minidom

from base import config

# Read a xml nodelist
def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return "".join(rc)

# Get information from an xml at 'events-list'
def get():
    try:
        xmldoc = minidom.parse(urllib.urlopen(config.get('events-list')))
        dname = xmldoc.getElementsByTagName('name')[0]
        dtime = xmldoc.getElementsByTagName('timestamp')[0]
        u_time = getText(dtime.childNodes)
        p_name = getText(dname.childNodes)
        utc_time = time.ctime(int(u_time))
        return p_name, str(utc_time)
        
    except Exception:
        return False
        
# Grab the utc time and convert it to something readable
def utc():
    d = datetime.utcnow()
    t = calendar.timegm(d.utctimetuple())
    return (str(time.ctime(t)))
