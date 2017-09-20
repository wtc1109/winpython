import urllib, urllib2, time
"""use post method to send a ucmq msg to server"""

test_data = {'name': 'testmq', 'opt':'put', 'ver':'2', 'data':'asdfih'}
test_data_encode = urllib.urlencode(test_data)
print test_data_encode
requrl = "http://192.168.7.130/?name=testmq&opt=put&ver=2"
res_data = urllib2.Request(requrl, data="641968489")
resp = urllib.urlopen(res_data.get_full_url(), data="sfsfsfsdf")
res = resp.read()
print res
resp.close()