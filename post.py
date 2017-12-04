import urllib, urllib2, time
"""use post method to send a ucmq msg to server"""

test_data = {'name': 'testmq', 'opt':'put', 'ver':'2', 'data':'asdfih'}
test_data_encode = urllib.urlencode(test_data)

requrl ="http://192.168.7.231/cgi-bin/setting.cgi"
res_data = urllib2.Request(requrl, data=test_data)
str_info = urllib.urlencode(test_data)
try:
    resp = urllib.urlopen(res_data.get_full_url(), data=str_info)
    res = resp.read()
    # print res
    resp.close()
except Exception, e:
    print e