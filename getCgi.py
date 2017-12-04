import urllib, urllib2, time
from HTMLParser import HTMLParser
data_link = []
tr_start = False
"""usr get method to get a ucmq msg from server"""
class MyHtmlParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        global tr_start, data_link
        print "<%s>"%tag
        if 'tr' == tag and tr_start == False:
            tr_start = True
        if 'input' == tag and True == tr_start:
            dic_val = dict(attrs)
            try:
                val = dic_val["value"]
                data_link.append(val)
            except:
                pass
    def handle_endtag(self, tag):
        global tr_start
        print "</%s>"%tag
        if 'tr' == tag:
            tr_start = False

    def handle_startendtag(self, tag, attrs):
        print "<%s/>"%tag
    def handle_data(self, tag):
        global tr_start
        print "data=", tag
        if True == tr_start:
            data_link.append(tag)

test_data = {'name': 'testmq', 'opt':'get', 'ver':'2', 'data':'asdfih'}
test_data_encode = urllib.urlencode(test_data)
print test_data_encode
test_data2 = {}
requrl = "http://192.168.7.31/cgi-bin/status.cgi"
res_data = urllib2.urlopen(requrl)
res = res_data.read()
print res
res_data.close()
urllib.urlcleanup()


parser = MyHtmlParser()
parser.feed(res)
print parser
print data_link
dic2 = {}
for i in range(len(data_link)/2):
    msg = data_link[2*i].strip(' ')
    msg = msg.strip('\r')
    msg = msg.strip('\n')
    if '' == msg:
        continue
#    print r'%x'%msg
    dic = {data_link[2*i]:data_link[2*i+1]}
    dic2.update(dic)
print dic2