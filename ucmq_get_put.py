import urllib, urllib2, time, json
"""use get method to send ucmq msg"""

data_str = {"sn":"123456787","ip":"192.168.7.185","pic_sn":"963185",\
            "location":"/info/111.jpg","type_for":"place", "exp":"12365",\
            "gain":"12.5", "slave":0,"neighbor":"123456788","bluetooch_id":"654321", "definition":"500", "why":"auto"}
data_json = json.dumps(data_str)
test_data = {'name': 'testmq', 'opt':'put', 'ver':'2', 'data':json.dumps(data_str)}
test_data_encode = urllib.urlencode(test_data)
data_str2 = {"sn":"123456789","ip":"192.168.7.231","pic_sn":"963186",\
            "location":"/images/test.jpg","type_for":"place", "exp":"12365",\
            "gain":"12.5", "slave":0,"neighbor":"123456790", "definition":"500", "why":"ai"}

print test_data_encode
test_data2 = {}
requrl = "http://192.168.7.19:8803/"
start = time.time()
print start
for i in range(50000):
    res_data = urllib2.urlopen(requrl + "?" + test_data_encode)
    res = res_data.read()
    res_data.close()
#    time.sleep(1)
    data_str2["pic_sn"] = str(time.time())
    test_data2 = {'name': 'testmq', 'opt': 'put', 'ver': '2', 'data': json.dumps(data_str2)}
    test_data_encode2 = urllib.urlencode(test_data2)
    res_data = urllib2.urlopen(requrl + "?" + test_data_encode2)
    res = res_data.read()
    res_data.close()
end_time = time.time()
print end_time
print end_time -start