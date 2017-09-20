import time, json, Queue, os
print time.asctime()
print time.gmtime()
buff = [1024]
_ip = ''
print _ip == None
attrs = []
attrs.append(("abc",'123'))
attrs.append(("abd",'234'))
attrs.append(("adc","saf"))
dic = dict(attrs)
gmtime1 = time.gmtime()
days = "%s%s"%(str(gmtime1.tm_mon).zfill(2), str(gmtime1.tm_mday).zfill(2))
localtime1 = time.localtime()

os.mkdir("d://hvcd")
print days
sec = "%s%s%s"%(str(localtime1.tm_hour).zfill(2), str(localtime1.tm_min).zfill(2), str(localtime1.tm_sec).zfill(2))
print sec
file = "d://hvcd/ip100/%s"% days + sec + ".jpg"
print file
i = 100
url_base0 = "http://192.168.1.%s/images/0.jpg"% i
#print url_base0
url_addr =[]
url_base1 = "http://192.168.1.%s/images/1.jpg" % i
url_addr.append(url_base0)
url_addr.append(url_base1)

print url_addr[1]
url_addr.append(url_base0)

str_json = json.dumps({"url":url_base1, "file":file})
print str_json
myQueue = Queue.Queue()
myQueue.put_nowait(str_json)
json_recv=myQueue.get()
recv_dic = json.loads(json_recv)
print recv_dic
print recv_dic["url"]
url_addr0 = []
url_addr1 = []

def init_url_addr():
    _url_addr0 = []
    _url_addr1 = []
    for i in range(100, 106):
        _url_base0 = "http://192.168.1.%s/images/0.jpg" % i
        _url_base1 = "http://192.168.1.%s/images/1.jpg" % i
        _url_addr0.append(_url_base0)
        _url_addr1.append(_url_base1)
    return _url_addr0, _url_addr1

def get_file_name():
    _localtime1 = time.localtime()
    _sec = "%s%s%s" % (
    str(_localtime1.tm_hour).zfill(2), str(_localtime1.tm_min).zfill(2), str(_localtime1.tm_sec).zfill(2))
    _days = "%s%s" % (str(_localtime1.tm_mon).zfill(2), str(_localtime1.tm_mday).zfill(2))
    _file_info = []
    for i in range(100, 106):
        file_name0 = "d://hvcd/ip%s/%s/" % (i, _days) + _sec + "_0.jpg"
        j = 0
        _dict1 = {"url": url_addr0[j], "file": file_name0}
        _file_info.append(json.dumps(_dict1))

        file_name1 = "d://hvcd/ip%s/%s/" % (i, _days) + _sec + "_1.jpg"
        _dict1 = {"url": url_addr1[j], "file": file_name1}
        _file_info.append(json.dumps(_dict1))
        j += 1
    return _file_info
url_addr0, url_addr1 = init_url_addr()
file_name = get_file_name()
print file_name