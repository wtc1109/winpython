import urllib, urllib2, time
"""usr get method to get a ucmq msg from server"""

test_data = {'name': 'testmq', 'opt':'get', 'ver':'2', 'data':'asdfih'}
test_data_encode = urllib.urlencode(test_data)
print test_data_encode
test_data2 = {}
requrl = "http://192.168.7.13:8803"
while True:
    res_data = urllib2.urlopen(requrl + '?' + test_data_encode)
    res = res_data.read()
    print res
res_data.close()
urllib.urlcleanup()
exit()