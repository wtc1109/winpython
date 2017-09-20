import urllib, urllib2, time, json
import os
"""receive ucmq messages and download the files to local d:\,running on Windowns
"""
DIRECTION_SAVE_FILES = "d://hvcd/"
def Download_file(jstr):
    _dic1 = json.loads(jstr)
    _url = "http://" + _dic1["ip"] + _dic1["location"]
    _ip_addr = _dic1["ip"].split('.')
    _file_name = "d://hvcd/ip" + _ip_addr[2] + '_' +_ip_addr[3]# + '/' + _dic1["id"] + '/' + _dic1["pic_sn"] + ".jpg"
    if not os.path.isdir(_file_name):
        try:
            os.mkdir(_file_name)
        except Exception, e:
        #maybe anther thread is making dir, or no right to do so
            if not os.path.isdir(_file_name):
                return
    _file_name += '/' + _dic1["id"]
    if not os.path.isdir(_file_name):
        try:
            os.mkdir(_file_name)
        except Exception, e:
            if not os.path.isdir(_file_name):
                return

    _localtime1 = time.localtime()
    days = "%s%s" % (str(_localtime1.tm_mon).zfill(2), str(_localtime1.tm_mday).zfill(2))
    _file_name += '/' + days
    if not os.path.isdir(_file_name):
        try:
            os.mkdir(_file_name)
        except Exception, e:
            if not os.path.isdir(_file_name):
                return

    _file_name += '/' + _dic1["pic_sn"] + ".jpg"
    print _file_name
#    _url = "http://192.168.7.185/info/hub.c"
    try:
        fd, info = urllib.urlretrieve(_url, _file_name)
    except Exception, e:
        print e
        return
    try:
        length = info.dict["content-length"]
        print info.dict["content-length"]
    except KeyError, IOError:
        os.remove(_file_name)

test_data = {'name': 'testmq', 'opt':'get', 'ver':'2'}
test_data_encode = urllib.urlencode(test_data)
print test_data_encode
test_data2 = {}
requrl = "http://192.168.7.19:8803"
j = 10
print time.time()
while j > 0:
    try:
        res_data = urllib2.urlopen(requrl + '?' + test_data_encode)
    except urllib2.URLError, e:
        print e
        time.sleep(2)
        continue

    res = res_data.read()
    mq_str = res.split('\n')
    print mq_str[0]
    ret_str = mq_str[0].rstrip('\r')
    if (ret_str == "UCMQ_HTTP_OK"):
        Download_file(mq_str[1])
        dic1 = json.loads(mq_str[1])
        print "OK"
    elif (ret_str == "UCMQ_HTTP_ERR_QUE_EMPTY"):
        time.sleep(1)
    res_data.close()
    urllib.urlcleanup()
    j -= 1
print time.time()
exit()