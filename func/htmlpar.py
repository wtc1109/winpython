#import HTMLParser
from HTMLParser import HTMLParser
data_link = []
tr_start = False

class MyHtmlParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        global tr_start, dic_cnt
        print "<%s>"%tag
        if 'td' == tag and tr_start == False:
            tr_start = True
    def handle_endtag(self, tag):
        global tr_start
        print "</%s>"%tag
        tr_start = False

    def handle_startendtag(self, tag, attrs):
        print "<%s/>"%tag
    def handle_data(self, tag):
        global tr_start, tr_start
        print "data=", tag
        if True == tr_start:
            data_link.append(tag)

files = """<html><head><meta http-equiv='content-type' content='text/html; charset=gb2312'><title>version_number</title></head>
        <style type='text/css'>.board {width:80px;height:25px}.board1{width:150px;height:30px}.board2{width:400px;height:px}</style>
        <body topmargin=150px><table border=0 cellpadding=0 cellspacing=0 align= 'center' style='width:550px;'>
        <tr><td class=board1>BIOS</td><td class=board2>00000000</td></tr>
        <tr><td class=board1>RK_HUB</td><td class=board2>RK_HUB Aug 10 2017</td></tr>
        <tr><td class=board1>RK_SYS</td><td class=board2>RK_SYS Jul 18 2017</td></tr>
        <tr><td class=board1> </td><td class=board2> </td></tr>
        <tr><td class=board1>BOA</td><td class=board2>BOA_a20_2017_0809</td></tr>
        </table></body></html>"""
parser = MyHtmlParser()
parser.feed(files)
print parser
print data_link
dic2 = {}
for i in range(len(data_link)/2):
    msg = data_link[2*i].strip(' ')
    if '' == msg:
        continue
#    print r'%x'%msg
    dic = {data_link[2*i]:data_link[2*i+1]}
    dic2.update(dic)
print dic2