import threading, Queue, urllib, json, time

gQueues = []
for i in range(10):
    Info_queue = Queue.Queue(maxsize=5)
    gQueues.append(Info_queue)
gQueue_ret = Queue.Queue(maxsize=20)

class download_thread(threading.Thread):
    def __init__(self, idnum):
        self.id = idnum
        self.url_addr = []
        self.file_name = []
        threading.Thread.__init__(self)
    def run(self):
        global gQueues, gQueue_ret
        try:
            _recv_json = gQueues[self.id].get(block=True, timeout=5)
            print "***********"
            print _recv_json
        except Exception, e:
            #print str(e)
            print str(self.name)
            time.sleep(1)
            exit()
        recv_dict = json.loads(_recv_json)
        self.url_addr = recv_dict["url"]
        self.file_name = recv_dict["file"]

        print "thread %d "%self.id +self.url_addr +self.file_name
        step = 0
        try:
            fd, info = urllib.urlretrieve(url=self.url_addr, filename= self.file_name)
        except IOError, e:
            step = -1
            ret_str = str(e)
            print e
        finally:
            if step > 0:
                gQueue_ret.put(json.dumps({"ret": 1}))
            else:
                gQueue_ret.put(json.dumps({"ret": ret_str}))
if __name__ == '__main__':
    threads = []
    for i in range(10):
        thread = download_thread(i)
        thread.start()
        threads.append(thread)
    dict1={"url":"192.168.1.100", "file":"123.txt"}
    gQueues[3].put_nowait(json.dumps(dict1))
    rec_json = gQueue_ret.get(block=100)
    print rec_json