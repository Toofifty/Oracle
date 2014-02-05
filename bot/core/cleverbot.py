import urllib2
from hashlib import md5
import re
 
class ServerFullError(Exception):
        pass
 
class Session:
    ReplyFlagsRE = re.compile('<INPUT NAME=(.+?) TYPE=(.+?) VALUE="(.*?)">', re.IGNORECASE | re.MULTILINE)
    cleverargs = {
        'stimulus' : '',
        'start' : 'y',
        'sessionid' : '',
        'vText8' : '',
        'vText7' : '',
        'vText6' : '',
        'vText5' : '',
        'vText4' : '',
        'vText3' : '',
        'vText2' : '',
        'icognoid' : 'wsf',
        'icognocheck' : '',
        'prevref' : '',
        'emotionaloutput' : '',
        'emotionalhistory' : '',
        'asbotname' : '',
        'ttsvoice' : '',
        'typing' : '',
        'lineref' : '',
        'sub' : 'Say',
        'islearning' : '1',
        'cleanslate' : 'false'
    }
    headers = {
        'User-Agent' : 'Mozilla/5.0 (X11; U; Linux x86_64; it; rv:1.9.1.8) Gecko/20100214 Ubuntu/9.10 (karmic) Firefox/3.5.8',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language' : 'it-it,it;q=0.8,en-us;q=0.5,en;q=0.3',
        'X-Moz' : 'prefetch',
        'Accept-Charset' : 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
        'Referer' : 'http://www.cleverbot.com',
        'Cache-Control' : 'no-cache, no-cache',
        'Pragma' : 'no-cache'
    }
    MsgList = []
 
    def __init__(self):
        self.safe_map = build_safe_map()
 
    #Sends request to Cleverbot and retrieves response
    def Send(self):
            data = self.encode(self.cleverargs)
            digest_txt = data[9:29]
            hash = md5(digest_txt).hexdigest()
            self.cleverargs['icognocheck'] = hash
            data = self.encode(self.cleverargs)
            req = urllib2.Request("http://www.cleverbot.com/webservicefrm",data,self.headers)
            f = urllib2.urlopen(req)
            return f.read()
 
    def Ask(self,q):
            self.cleverargs['stimulus'] = q
            if self.MsgList:
                self.cleverargs['lineref'] = '!0'+str(len(self.MsgList)/2)
            ans = self.Send()
            if '<meta name="description" content="Jabberwacky server maintenance">' in ans:
                raise ServerFullError, "The Cleverbot server answered with full load error"
            self.MsgList += [q]
            answ_dict = self.GetAnswerArgs(ans)
            for key in answ_dict:
                    try:
                        self.cleverargs[key] = answ_dict[key]
                    except:
                        pass
            self.cleverargs['emotionaloutput'] = ''
            reply_i=ans.find('<!-- Begin Response !-->')+25
            reply_s=ans.find('<!-- End Response !-->')
            self.MsgList += [ans[reply_i:reply_s]]
            return ans[reply_i:reply_s]
 
    #runs the compiled regex and places responses in a dictionary
    def GetAnswerArgs(self, text):
        results = self.ReplyFlagsRE.findall(text)
        args = {}
        for r in results:
            args[r[0]]=r[2]
        return args
 
    #writes the current dictionary args to a URL string
    def encode(self,data):
        text=''
        for key in data:
            v = self.sanitize(data[key])
            text+='&'+key+'='+v
        return text[1:]
 
    #replaces unsafe characters with safe versions for the URL string
    def sanitize(self,s):
        res = map(self.safe_map.__getitem__, s)
        return ''.join(res)
 
#caches a map of safe characters
def build_safe_map():
    safe = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'
           'abcdefghijklmnopqrstuvwxyz', '0123456789', '_.-')
    safe_map = {}
    for i in range(256):
        c = chr(i)
        safe_map[c] = (c in safe) and c or ('%%%02X' % i)
    return safe_map
 
if __name__ == '__main__':
    cb1 = Session()
    cb2 = Session()
 
    begin = cb1.Ask("Hello")
    print "- " + begin
    it1 = cb2.Ask(begin)
    print "- " + it1
 
    while True:
        it2 = cb1.Ask(it1)
        print "- " + it2
        it1 = cb2.Ask(it2)
        print "- " + it1