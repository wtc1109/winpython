import urllib, urllib2, time
import json
"""use post method to send a ucmq msg to server"""

test_data = {'name': 'testmq', 'opt':'put', 'ver':'2', 'data':'asdfih'}
test_data_encode = urllib.urlencode(test_data)
print test_data_encode
requrl = "http://192.168.7.130/cgi-bin/param_set.cgi"
res_data = urllib2.Request(requrl, data=json.dumps(test_data))
str_info = "name1=1&name2=2&name3=3"
resp = urllib.urlopen(res_data.get_full_url(), data=str_info)
res = resp.read()
print res
resp.close()