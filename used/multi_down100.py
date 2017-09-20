import threading, Queue, urllib, json, os, time
"""use THREAD_NUM threads for download pictures, for ip=192.168.1.EQUIPMENT_IP_START to
192.168.1.EQUIPMENT_IP_END every 5 second forever"""
THREAD_NUM = 10 #how many threads
EQUIPMENT_IP_START = 100
EQUIPMENT_IP_END = 120
INTERVAL_2_PIC_SECOND = 10  #interval time of two pictures in second
gQueues = []
gThread_using_flag = []
for i in range(THREAD_NUM):
    Info_queue = Queue.Queue(maxsize=5)
    gQueues.append(Info_queue)
gQueue_ret = Queue.Queue(maxsize=40)

start_time = time.localtime()
url_addr0 = []
url_addr1 = []

def write_err_log(e, str):
    """write error log to a file for debug further"""
    print e
    print str

def init_url_addr():
    _url_addr0 = []
    _url_addr1 = []
    for i in range(EQUIPMENT_IP_START, EQUIPMENT_IP_END):
        _url_base0 = "http://192.168.7.%s/images/test.jpg" % i
        _url_base1 = "http://192.168.7.%s/images/1.jpg" % i
        _url_addr0.append(_url_base0)
        _url_addr1.append(_url_base1)
    return _url_addr0, _url_addr1

def mk_download_dirs():
    """a new day ,so a new direction is necessary"""
    _localtime1 = time.localtime()
    days = "%s%s" % (str(_localtime1.tm_mon).zfill(2), str(_localtime1.tm_mday).zfill(2))
    for i in range(EQUIPMENT_IP_START, EQUIPMENT_IP_END):
        if os.path.isdir("c://hvcd/ip%s"%(i)):
            pass
        else:
            os.mkdir("c://hvcd/ip%s"%(i))

        if os.path.isdir("c://hvcd/ip%s/%s"% (i, days)):
            pass
        else:
            os.mkdir("c://hvcd/ip%s/%s"% (i, days))



def get_file_name():
    """as local time, we want to save files name """
    _localtime1 = time.localtime()
    _sec = "%s%s%s" % (
    str(_localtime1.tm_hour).zfill(2), str(_localtime1.tm_min).zfill(2), str(_localtime1.tm_sec).zfill(2))
    _days = "%s%s" % (str(_localtime1.tm_mon).zfill(2), str(_localtime1.tm_mday).zfill(2))
    _file_info = []
    j = 0
    for i in range(EQUIPMENT_IP_START, EQUIPMENT_IP_END):
        _file_name = "c://hvcd/ip%s/%s/" % (i, _days) + _sec + "_0.jpg"
        _dict1 = {"url": url_addr0[j], "file": _file_name}
        _file_info.append(json.dumps(_dict1))
        """
        _file_name = "c://hvcd/ip%s/%s/" % (i, _days) + _sec + "_1.jpg"
        _dict1 = {"url": url_addr1[j], "file": _file_name}
        _file_info.append(json.dumps(_dict1))"""
        j += 1
    return _file_info

def download_pics():
    global start_time, gThread_using_flag
    while True:
        _localtime1 = time.localtime()
        _time_start_sec = time.time()
        if _localtime1.tm_hour < start_time.tm_hour:
            mk_download_dirs()  #if new days make new direction
            start_time = _localtime1
        else:
            start_time = _localtime1

        _file_info = []
        _file_info = get_file_name()

        j = 12
        print "start download %d files time="%len(_file_info) + str(time.time())
        while len(_file_info):
#            print "put queue start " + str(time.time())
            for i in range(THREAD_NUM):
                if gThread_using_flag[i] == 1 and len(_file_info):
                    gQueues[i].put_nowait(_file_info.pop())
                    gThread_using_flag[i] = 0
#                    print "put queue end " + str(i) + " " + str(time.time()) + " list len " + str(len(_file_info))

            while gQueue_ret.empty():
                time.sleep(0.2)
            for i in range(THREAD_NUM):
                if gQueue_ret.empty():
                    break
                try:
                    rec_json = gQueue_ret.get(block=False)
                    gThread_using_flag[json.loads(rec_json)["id"]] = 1

#                    print "Queue get " + rec_json
                except IOError, Queue.Empty:
                    break

        _time_diff = time.time() - _time_start_sec
        if _time_diff < INTERVAL_2_PIC_SECOND:
            time.sleep(INTERVAL_2_PIC_SECOND - _time_diff)
            print "sleep %d"%(INTERVAL_2_PIC_SECOND - _time_diff)
        print "end download time=%s, use %d sec"%(str(time.time()), _time_diff)
class DownloadThread(threading.Thread):
    def __init__(self, idnum):
        self.__id = idnum
        self.__url_addr = []
        self.__file_name = []
        threading.Thread.__init__(self)
    def run(self):
        global gQueues, gQueue_ret
        while True:
            _recv_json = gQueues[self.__id].get(block=True)
            _recv_dict = json.loads(_recv_json)
            self.__url_addr = _recv_dict["url"]
            self.__file_name = _recv_dict["file"]
            #print "Child get url=" + str(self.__url_addr) +" save to " + str(self.__file_name)
            step = 1
            try:
                fd, info = urllib.urlretrieve(url=self.__url_addr, filename= self.__file_name)
            except Exception, e:
                step = -1
                ret_str = str(e)
                print e, self.__url_addr
            finally:
                if step > 0:
                    try:
                        length = info.dict["content-length"]  # if length is 0,so remove the empty file
                    except KeyError:
                        os.remove(self.__file_name)
                    gQueue_ret.put(json.dumps({"ret": 1, "id": self.__id}))
                else:
                    gQueue_ret.put(json.dumps({"ret": ret_str, "id": self.__id}))
                #print "child end  @" + str(self.__id) +" time="+ str(time.time())

if __name__ == '__main__':

    if os.path.isdir("c://hvcd"):
        pass
    else:
        os.mkdir("c://hvcd")
    mk_download_dirs()
    url_addr0, url_addr1 = init_url_addr()
    threads = []
    for i in range(THREAD_NUM):
        flag = 1
        gThread_using_flag.append(flag)
        thread = DownloadThread(i)
        thread.start()
        threads.append(thread)
    download_pics()

