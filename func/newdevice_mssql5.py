import socket
import threading
import time
import json
import pymssql
import datetime
import Queue
import urllib,os
import requests, ConfigParser
import wtclib_mssql, hvpd_status

THREAD_NUM = 5 #how many threads


def get_a_mssql_cur_forever():
    while True:
        (ret, err)=wtclib_mssql.get_a_mssql_cur_once("conf.ini")
        if None != ret:
            return ret
        else:
            print (err)
            time.sleep(20)

def udp_recv_is_json(data):
    if isinstance(data, str):
        try:
            _dict1 = json.loads(data)
            return _dict1
        except Exception, e:
            mylog.debug(str(e)+":"+data)
            return None
    else:
        mylog.debug("udp recv %s is not str,len=%d"%(data, len(data)))
        return None

class Mssql:
    def __Connect(self):
        self.conn = get_a_mssql_cur_forever()
        try:
            cur = self.conn.cursor()
        except Exception, e:
            print (str(e))
            return None
        return cur
    def select(self, sql):
        try:
            cur = self.__Connect()
            if None == cur:
                return ''
            cur.execute(sql)
            rows = cur.fetchall()
            cur.close()
            self.conn.close()
            return rows
        except Exception, e:
            print (str(e))
            return ''
    def insert(self, sql):
        try:
            cur = self.__Connect()
            if None == cur:
                return -2
            cur.execute(sql)
            cur.close()
            self.conn.commit()
            self.conn.close()
            return 0
        except Exception, e:
            print (str(e))
            return -1


def udp_recv_data_process(dictin, mylog):
    global gThread_using_flag, gQueues
    _timeSec = int(time.time())
    mssql = Mssql()
    Sn_len = len(dictin["sn"])
    if Sn_len < 8:
        return None

    if Sn_len < 14:
        _sql = "if not EXISTS (SELECT cameraID FROM dbo.hvpdOnline1 WHERE cameraID='%s') " \
               "insert dbo.hvpdOnline1(cameraID,ip, reNewTimet) values('%s','%s',%d)" \
               "else update dbo.hvpdOnline1 set ip='%s',reNewTimet=%d, reNewDate=getdate() where cameraID='%s';"\
               %(dictin["sn"], dictin["sn"], dictin["ip"], _timeSec,dictin["ip"], _timeSec,dictin["sn"])
        mssql.insert(_sql)
        _sql = "select * from dbo.hvpdOnline1 where cameraID='%s';"%(dictin["sn"])
        _hvpds = mssql.select(_sql)
        need_upgrade = 0
        if 0 == len(_hvpds):
            need_upgrade = 1
        else:
            _hvpd = _hvpds[0]
            if _timeSec - _hvpd[3] > 3600:
                need_upgrade = 1

        if 0 != need_upgrade:
            for i in range(THREAD_NUM):
                if 0 != gThread_using_flag[i]:
                    _dic = {"ip":dictin["ip"], "sn":dictin["sn"]}
                    gQueues[i].put_nowait(json.dumps(_dic))
                    gThread_using_flag[i] = 0
                    break
        return 0


    try:
        _localTime = time.localtime()
        _year = _localTime.tm_year - 2000
        _mon = _localTime.tm_mon
        _sql = "select * from dbo.IPNC where HardVer='%s';"%dictin["sn"]
        now1 = datetime.datetime.now()
        a1 = mssql.select(sql=_sql)
        if 0 == len(a1):#new hvpd3 device
            _sql = "SELECT max(MacIndex) FROM dbo.IPNC;"
            _maxMAC = mssql.select(_sql)[0][0]
            _sql = "select max(ID) from dbo.IPNC where DeviceTypeID=430;"
            _maxID = mssql.select(_sql)[0][0]
            _year_mon = "%02d%02d" % (_year, _mon)
            if _year_mon == _maxID[0:4]:
                _len_sn = len(_maxID)
                _sn_int = int(_maxID[_len_sn - 4: _len_sn])
            else:
                _sn_int = -1
            if 0 == (_sn_int % 2):
                _sn_int += 1
            else:
                _sn_int += 2
            _sn_str = "%s43%04d" % (_year_mon, _sn_int)
            _macShort = _maxMAC+1
            _macStr = "%06X" % _macShort
            _mac = "00-1B-38-%s-%s-%s" % (_macStr[0:2], _macStr[2:4], _macStr[4:6])
            _dict_msg = {"reboot": 1, "Fsn": "%s" % _sn_str, "FMAC": "%s" % _mac}
            #now = datetime.datetime.now()
            if not "neighbor" in dictin:
                _sql = "insert into dbo.IPNC(ID,MacIndex,HardVer,DeviceTypeID,Manuday,mYear,mMonth,mIndex,Mac1,Mac2,Mac3)" \
                       "values('%s',%d,'%s',430,getdate(),%d,%d,%d, %s,%s,%s)" \
                       % (_sn_str, _macShort, dictin["sn"], now1.year, now1.month, _sn_int,int(_macStr[0:2],16), int(_macStr[2:4],16), int(_macStr[4:6],16))
                mssql.insert(_sql)
            elif len(dictin["neighbor"]) < 14:
                _sql = "insert into dbo.IPNC(ID,MacIndex,HardVer,DeviceTypeID,Manuday,mYear,mMonth,mIndex,Mac1,Mac2,Mac3)" \
                       "values('%s',%d,'%s',430,getdate(),%d,%d,%d, %s,%s,%s)" \
                       % (_sn_str, _macShort, dictin["sn"], now1.year, now1.month, _sn_int,int(_macStr[0:2],16), int(_macStr[2:4],16), int(_macStr[4:6],16))
                mssql.insert(_sql)
            else:
                _sn_str2 = "%s43%04d" % (_year_mon, _sn_int+1)
                _macShort2 = _maxMAC + 2
                _macStr2 = "%06X" % _macShort2
                _mac2 = "00-1B-38-%s-%s-%s" % (_macStr2[0:2], _macStr2[2:4], _macStr2[4:6])
                _sql = "select * from dbo.IPNC where HardVer='%s'"%dictin["neighbor"]
                _neighbor = mssql.select(_sql)
                if 0 == len(_neighbor):
                    if max(dictin["neighbor"], dictin["sn"]) == dictin["neighbor"]:
                        _sql = "insert into dbo.IPNC(ID,MacIndex,HardVer,DeviceTypeID,Manuday,mYear,mMonth,mIndex,Mac1,Mac2,Mac3)" \
                               "values('%s',%d,'%s',430,getdate(),%d,%d,%d, %d,%d,%d)" \
                               % (_sn_str, _macShort, dictin["sn"], now1.year, now1.month, _sn_int,int(_macStr[0:2],16), int(_macStr[2:4],16), int(_macStr[4:6],16))
                        mssql.insert(_sql)
                        _sql = "insert into dbo.IPNC(ID,MacIndex,HardVer,DeviceTypeID,Manuday,mYear,mMonth,mIndex,Mac1,Mac2,Mac3)" \
                               "values('%s',%d,'%s',430,getdate(),%d,%d,%d, %d,%d,%d)" \
                               % (_sn_str2, _macShort2, dictin["neighbor"], now1.year, now1.month, _sn_int+1,int(_macStr2[0:2],16), int(_macStr2[2:4],16), int(_macStr2[4:6],16))
                        mssql.insert(_sql)
                    else:
                        _sql = "insert into dbo.IPNC(ID,MacIndex,HardVer,DeviceTypeID,Manuday,mYear,mMonth,mIndex,Mac1,Mac2,Mac3)" \
                               "values('%s',%d,'%s',430,getdate(),%d,%d,%d, %d,%d,%d)" \
                               % (_sn_str, _macShort, dictin["neighbor"], now1.year, now1.month, _sn_int,int(_macStr[0:2],16), int(_macStr[2:4],16), int(_macStr[4:6],16))
                        mssql.insert(_sql)
                        _sql = "insert into dbo.IPNC(ID,MacIndex,HardVer,DeviceTypeID,Manuday,mYear,mMonth,mIndex,Mac1,Mac2,Mac3)" \
                               "values('%s',%d,'%s',430,getdate(),%d,%d,%d, %d,%d,%d)" \
                               % (_sn_str2, _macShort2, dictin["sn"], now1.year, now1.month, _sn_int+1,int(_macStr2[0:2],16), int(_macStr2[2:4],16), int(_macStr2[4:6],16))
                        mssql.insert(_sql)
                        _dict_msg = {"reboot": 1, "Fsn": "%s" % _sn_str2, "FMAC": "%s" % _mac2}
                else:   #neighbor has already here,so only insert sn is enough
                    _sql = "insert into dbo.IPNC(ID,MacIndex,HardVer,DeviceTypeID,Manuday,mYear,mMonth,mIndex,Mac1,Mac2,Mac3)" \
                           "values('%s',%d,'%s',430,getdate(),%d,%d,%d, %d,%d,%d)" \
                           % (_sn_str, _macShort, dictin["sn"], now1.year, now1.month, _sn_int,int(_macStr[0:2],16), int(_macStr[2:4],16), int(_macStr[4:6],16))
                    mssql.insert(_sql)
        else:#have a sn before, reset once again
            _hvpd = a1[0]
            _macShort = _hvpd[5]
            _macStr = "%06X"%_macShort
            _mac = "00-1B-38-%s-%s-%s"%(_macStr[0:2], _macStr[2:4], _macStr[4:6])
            _dict_msg={"reboot":1,"Fsn":"%s"%_hvpd[0],"FMAC":"%s"%_mac}

            _sql = "if not EXISTS (SELECT cameraID FROM dbo.hvpdOnline1 WHERE cameraID='%s') " \
                   "insert dbo.hvpdOnline1(cameraID,ip, reNewTimet) values('%s','%s',%d)" \
                   "else update dbo.hvpdOnline1 set ip='%s',reNewTimet=%d where cameraID='%s'" \
                   % (_hvpd[0], _hvpd[0], dictin["ip"], _timeSec, dictin["ip"], _timeSec, _hvpd[0])
            mssql.insert(_sql)
    except Exception, e:
        mylog.debug(str(e))
        return None
    socket.setdefaulttimeout(1)
    wtclib_mssql.http_get_cgi_msg2device(_dict_msg, dictin["ip"], "setting")


def get_version_file(fi, hardver):
    cf = ConfigParser.ConfigParser()
    try:
        cf.read(fi)
        secs = cf.sections()
        opts = cf.options(hardver)
        uart_version = cf.get(hardver, "UART_VERSION")
        udp_version = cf.get(hardver, "UDP_VERSION")
        camera_version = cf.get(hardver, "CAMERA_VERSION")
        fo = cf.get(hardver, "file")
        return uart_version, udp_version, camera_version, fo
    except Exception, e:
        print str(e)
        return '','','',''

class DownloadThread(threading.Thread):
    def __init__(self, idnum):
        self.__id = idnum
        threading.Thread.__init__(self)
    def run(self):
        global gQueues, gQueue_ret

        while True:
            _recv_json = gQueues[self.__id].get(block=True)
            _recv_dict = json.loads(_recv_json)
            _status_url = "http://"+_recv_dict["ip"]+"/cgi-bin/status.cgi"
            _status_dict = hvpd_status.get_hvpd_status(_status_url)
            if not "Fsn" in _status_dict:
                _ret_dic = {"id": self.__id, 'ret': -3, "sn": _recv_dict["sn"]}
                gQueue_ret.put(json.dumps(_ret_dic))
                continue
            if not "UART_VERSION" in _status_dict:
                _status_dict.update({"UART_VERSION":'0'})
            if not "UDP_VERSION" in _status_dict:
                _status_dict.update({"UDP_VERSION": '0'})
            if not "CAMERA_VERSION" in _status_dict:
                _status_dict.update({"CAMERA_VERSION": '0'})
            if not "HARDVER" in _status_dict:
                _status_dict.update({"HARDVER": '0'})
            if '2' == _status_dict["HARDVER"]:
                hardver = "version2"
            elif '3' == _status_dict["HARDVER"]:
                hardver = "version3"
            else:
                hardver = "version0"
            uart_version, udp_version, camera_version, upgrade_file = get_version_file("hvpd/version.ini", hardver)
            if '' == uart_version:
                _ret_dic = {"id": self.__id, 'ret': -2, "sn": _recv_dict["sn"]}
                gQueue_ret.put(json.dumps(_ret_dic))
                continue
            if _status_dict["CAMERA_VERSION"] == uart_version and   \
                _status_dict["UDP_VERSION"] == udp_version and  \
                _status_dict["UART_VERSION"] == camera_version:
                _ret_dic = {"id": self.__id, 'ret': 0, "sn": _recv_dict["sn"]}
                gQueue_ret.put(json.dumps(_ret_dic))
                continue
            socket.setdefaulttimeout(2)
            try:
                _upgrade_url = "http://"+_recv_dict["ip"]+"/cgi-bin/upgrade.cgi"
                files = {"filename": ("123.zip", open("hvpd/"+upgrade_file, "rb"))}
                r = requests.post(url=_upgrade_url, files=files)
                ret = 0
            except Exception, e:
                #print str(e)
                ret = str(e)
            _ret_dic = {"id": self.__id, 'ret':ret, "sn":_recv_dict["sn"]}
            gQueue_ret.put(json.dumps(_ret_dic))

class Udp_broadcast_receiver(threading.Thread):
    def __init__(self, ip):
        self.__ip = ip
        threading.Thread.__init__(self)
    def run(self):
        global gQueues, mylog
        _udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        _udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        ADDR = (self.__ip, 9982)
        while True:
            try:
                _udp_sock.bind(ADDR)
                break
            except Exception, e:
                mylog.debug("UDP bind Error %s,"%self.__ip + str(e))
                time.sleep(10)
        udp_cnt = 0
        _udp_sock.settimeout(60)
        while True:
            try:
                (data, addr) = _udp_sock.recvfrom(1024)
            except Exception, e:
                mylog.warning("udp receive " + str(e))
                # time.sleep(10)
                continue
            mylog.debug(data)
            _dict = udp_recv_is_json(data)
            if None != _dict:
                mylog.debug(data)
                info = udp_recv_data_process(_dict, mylog)

            msg = "nothing"
            _udp_sock.sendto(msg, addr)

if __name__ == '__main__':

    mylog = wtclib_mssql.create_logging('SetupUdpserver.log')
    mylog.info("udp is running start")
    mssql = Mssql()

    _sql = "create table dbo.hvpdOnline1(" \
           "cameraID char(24) primary key," \
           "ip char(24) not null," \
           "reNewTimet int default 0," \
           "upgradeTimet int default 0," \
           "reNewDate DATETIME default getdate());"
    mssql.insert(_sql)

    gQueues = []
    for i in range(THREAD_NUM):
        Info_queue = Queue.Queue(maxsize=5)
        gQueues.append(Info_queue)
    gQueue_ret = Queue.Queue(maxsize=20)
    threads = []
    thread_idles = THREAD_NUM
    gThread_using_flag = []
    for i in range(THREAD_NUM):
        flag = 1
        gThread_using_flag.append(flag)
        thread = DownloadThread(i)
        thread.start()
        threads.append(thread)

    name1 = socket.gethostname()
    _info = socket.gethostbyname_ex(name1)
    for _ip in _info[2]:
        _ip_dot = _ip.split('.')
        if '1' == _ip_dot[3]:
            continue
        thread = Udp_broadcast_receiver(_ip)
        mylog.info("UDP receiver @"+_ip)
        thread.start()
    time.sleep(0.5)

    while True:
        _timeSecInt = int(time.time())
        try:
            Cur_qsize = gQueue_ret.qsize()
            for i in range(Cur_qsize):
                try:
                    rec_json = gQueue_ret.get(block=False)
                    print "Queue get="+rec_json
                    recv_dict = json.loads(rec_json)
                    gThread_using_flag[recv_dict["id"]] = 1
                    if 0 == recv_dict["ret"]:
                        _sql = "update dbo.hvpdOnline1 set upgradeTimet=%d where cameraID='%s';"%(_timeSecInt, recv_dict["sn"])
                        mssql.insert(_sql)
                        mylog.info("upgrade %s firmware"%recv_dict["sn"])
                except IOError, Queue.Empty:
                    pass
        except Exception, e:
            mylog.warning("Queue get "+str(e))
            #time.sleep(10)
            continue
            mylog.debug(data)
        time.sleep(0.5)
