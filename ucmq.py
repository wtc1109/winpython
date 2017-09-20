import urllib


test_data = {'name':'testmq','opt':'status','ver':'2'}
test_data_urlencode = urllib.urlencode(test_data)
print(test_data_urlencode)
requrl = "http://192.168.7.19:8803"

#req = urllib.Request(url=requrl, data=test_data_urlencode)
#req.add_header('Referer', 'http://www.python.org/')
#print (req)
response = urllib.urlopen(requrl, data=test_data_urlencode)
print response.read()
response.close()
#res_data = urllib.urlopen(req)
#res = res_data.read()
#print (res)