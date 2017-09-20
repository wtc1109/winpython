import os, urllib, time

start_time = time.localtime()
url_addr0 = []
url_addr1 = []

def write_err_log(e, str):
    """write error log to a file for debug further"""
    print e
    print str


def mk_download_dirs():
    """a new day ,so a new direction is necessary"""
    global url_addr0, url_addr1
    localtime1 = time.localtime()
    days = "%s%s" % (str(localtime1.tm_mon).zfill(2), str(localtime1.tm_mday).zfill(2))
    for i in range(100, 106):
        if os.path.isdir("d://hvcd/ip%s"%(i)):
            pass
        else:
            os.mkdir("d://hvcd/ip%s"%(i))

        if os.path.isdir("d://hvcd/ip%s/%s"% (i, days)):
            pass
        else:
            os.mkdir("d://hvcd/ip%s/%s"% (i, days))

        url_base0 = "http://192.168.1.%s/images/0.jpg"% i
        url_base1 = "http://192.168.1.%s/images/1.jpg" % i
        url_addr0.append(url_base0)
        url_addr1.append(url_base1)
def download_pics():
    global start_time
    while True:
        localtime1 = time.localtime()
        if localtime1.tm_hour < start_time.tm_hour:
            mk_download_dirs()
            start_time = localtime1
        else:
            pass
        sec = "%s%s%s" % (str(localtime1.tm_hour).zfill(2), str(localtime1.tm_min).zfill(2), str(localtime1.tm_sec).zfill(2))
        days = "%s%s" % (str(localtime1.tm_mon).zfill(2), str(localtime1.tm_mday).zfill(2))
        for i in range(100, 102):
            file_name0 = "d://hvcd/ip%s/%s/"%(i, days)  + sec + "_0.jpg"
            j = 0
            try:
                fd, info = urllib.urlretrieve(url_addr0[j], file_name0)
            except IOError, e:
                write_err_log(e, file_name0)
            finally:
                print "download 0 end"

            file_name1 = "d://hvcd/ip%s/%s/" % (i, days) + sec + "_1.jpg"
            try:
                fd, info = urllib.urlretrieve(url_addr1[j], file_name1)
            except IOError, e:
                write_err_log(e, file_name1)
            finally:
                print "download 1 end"
            j += 1
        time.sleep(5)

if __name__ == '__main__':
    if os.path.isdir("d://hvcd"):
        pass
    else:
        os.mkdir("d://hvcd")
    mk_download_dirs()
    download_pics()
    print "process end"
    exit()