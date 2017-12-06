import urllib, urllib2, time, json
"""use get method to send ucmq msg"""

data_str = {"sn":"1711430006","ip":"192.168.7.19","pic_sn":"963185",\
            "location":"/images/ai0.jpg","type_for":"place", "exp":"12365",\
            "gain":"125", "slave":0,"neighbor":"1823456788","bluetooth":"654321",
            "definition":"500", "why":"auto", "CMOS":0}
data_json = json.dumps(data_str)
test_data = {'name': 'downloadmq', 'opt':'put', 'ver':'2', 'data':json.dumps(data_str)}
test_data_encode = urllib.urlencode(test_data)
data_str2 = {"sn":"123d456789abc1","ip":"192.168.7.19","pic_sn":"963186",\
            "location":"/images/ai0.jpg","type_for":"place", "exp":"12365",\
            "gain":"125", "slave":0, "definition":"500", "why":"ai", "CMOS":1,"placeGet":0}

print test_data_encode
test_data2 = {}
requrl = "http://192.168.7.19:8803/"
start = time.time()
print start

data_str2["pic_sn"] = str(time.time())
test_data2 = {'name': 'downloadmq', 'opt': 'put', 'ver': '2', 'data': json.dumps(data_str2)}
test_data_encode2 = urllib.urlencode(test_data2)
for i in range(10000):
    res_data = urllib2.urlopen(requrl + "?" + test_data_encode)
    res = res_data.read()
    res_data.close()
    #time.sleep(0.2)

    res_data = urllib2.urlopen(requrl + "?" + test_data_encode2)
    res = res_data.read()
    res_data.close()
    #time.sleep(0.1)
end_time = time.time()
print end_time
print end_time -start