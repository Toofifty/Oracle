"""
Oracle - Event grabber
~ Toofifty
"""

import time
import calendar
from datetime import datetime
from xml.dom import minidom

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def get():
    try:
        xmldoc = minidom.parse(urllib.urlopen('http://rapidcraftmc.com/api.php?events'))
        dname = xmldoc.getElementsByTagName('name')[0]
        dtime = xmldoc.getElementsByTagName('timestamp')[0]
        u_time = getText(dtime.childNodes)
        p_name = getText(dname.childNodes)
        utc_time = str(time.ctime(int(u_time)))
        return p_name, utc_time
    except:
        return False
        
def utc():
    d = datetime.utcnow()
    return (str(time.ctime(calendar.timegm(d.utctimetuple()))))