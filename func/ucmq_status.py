import urllib, urllib2, time, json
"""use get method to send ucmq msg"""


test_data = {'name': 'downloadmq', 'opt':'status', 'ver':'2'}
test_data_encode = urllib.urlencode(test_data)
requrl = "http://192.168.7.19:8803/"
start = time.time()
res_data = urllib2.urlopen(requrl + "?" + test_data_encode)
res = res_data.read()
res_data.close()
#time.sleep(0.2)
retList = res.split("\n")
for rets in retList:
    if rets.find("Unread the number") > -1:
        Unread = rets.split(':')
        unreadNo = int(Unread[1])

test_data2 = {'name': 'downloadmq', 'opt':'status_json', 'ver':'2'}
test_data_encode2 = urllib.urlencode(test_data2)
requrl2 = "http://192.168.7.19:8803/"
res_data2 = urllib2.urlopen(requrl2 + "?" + test_data_encode2)
res2 = res_data2.read()
res_data2.close()

dict_status = json.loads(res2)
end_time = time.time()
print end_time
print end_time -start