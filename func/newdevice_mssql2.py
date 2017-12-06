import socket
import threading
import time
import json
import pymssql
import datetime


import wtclib_mssql

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
    _timeSec = int(time.time())
    mssql = Mssql()
    if len(dictin["sn"]) < 14:
        _sql = "if not EXISTS (SELECT cameraID FROM dbo.hvpdOnline WHERE cameraID='%s') " \
               "insert dbo.hvpdOnline(cameraID,ip, reNewTimet) values('%s','%s',%d)" \
               "else update dbo.hvpdOnline set ip='%s',reNewTimet=%d where cameraID='%s';"\
               %(dictin["sn"],dictin["sn"],dictin["ip"], _timeSec,dictin["ip"], _timeSec,dictin["sn"])
        #_sql = "update dbo.hvpdOnline set ip='%s',reNewTimet=%d where cameraID='%s';"%(dictin["ip"], _timeSec,dictin["sn"])
        mssql.insert(_sql)
        return 0
    try:
        _localTime = time.localtime()
        _year = _localTime.tm_year - 2000
        _mon = _localTime.tm_mon
        _sql = "select * from dbo.IPNC where HardVer='%s';"%dictin["sn"]

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
                _sql = "insert into dbo.IPNC(ID,MacIndex,HardVer,DeviceTypeID)" \
                       "values('%s',%d,'%s',430)" % (_sn_str, _macShort, dictin["sn"])
                mssql.insert(_sql)
            elif len(dictin["neighbor"]) < 14:
                _sql = "insert into dbo.IPNC(ID,MacIndex,HardVer,DeviceTypeID)" \
                       "values('%s',%d,'%s',430)" % (_sn_str, _macShort, dictin["sn"])
                mssql.insert(_sql)
            else:
                _sn_str2 = "%s43%04d" % (_year_mon, _sn_int+1)
                _macShort2 = _maxMAC + 2
                _macStr2 = "%06X" % _macShort
                _mac2 = "00-1B-38-%s-%s-%s" % (_macStr2[0:2], _macStr2[2:4], _macStr2[4:6])
                _sql = "select * from dbo.IPNC where HardVer='%s'"%dictin["neighbor"]
                _neighbor = mssql.select(_sql)
                if 0 == len(_neighbor):
                    if max(dictin["neighbor"], dictin["sn"]) == dictin["neighbor"]:
                        _sql = "insert into dbo.IPNC(ID,MacIndex,HardVer,DeviceTypeID)" \
                               "values('%s',%d,'%s',430)" % (_sn_str, _macShort, dictin["sn"])
                        mssql.insert(_sql)
                        _sql = "insert into dbo.IPNC(ID,MacIndex,HardVer,DeviceTypeID)" \
                               "values('%s',%d,'%s',430)" % (_sn_str2, _macShort2, dictin["neighbor"])
                        mssql.insert(_sql)
                    else:
                        _sql = "insert into dbo.IPNC(ID,MacIndex,HardVer,DeviceTypeID)" \
                               "values('%s',%d,'%s',430)" % (_sn_str, _macShort, dictin["neighbor"])
                        mssql.insert(_sql)
                        _sql = "insert into dbo.IPNC(ID,MacIndex,HardVer,DeviceTypeID)" \
                               "values('%s',%d,'%s',430)" % (_sn_str2, _macShort2, dictin["sn"])
                        mssql.insert(_sql)
                        _dict_msg = {"reboot": 1, "Fsn": "%s" % _sn_str2, "FMAC": "%s" % _mac2}
                else:   #neighbor has already here,so only insert sn is enough
                    _sql = "insert into dbo.IPNC(ID,MacIndex,HardVer,DeviceTypeID)" \
                           "values('%s',%d,'%s',430)" % (_sn_str, _macShort, dictin["sn"])
                    mssql.insert(_sql)
        else:#have a sn before, reset once again
            _hvpd = a1[0]
            _macShort = _hvpd[5]
            _macStr = "%06X"%_macShort
            _mac = "00-1B-38-%s-%s-%s"%(_macStr[0:2], _macStr[2:4], _macStr[4:6])
            _dict_msg={"reboot":1,"Fsn":"%s"%_hvpd[0],"FMAC":"%s"%_mac}

            _sql = "if not EXISTS (SELECT cameraID FROM dbo.hvpdOnline WHERE cameraID='%s') " \
                   "insert dbo.hvpdOnline(cameraID,ip, reNewTimet) values('%s','%s',%d)" \
                   "else update [dbo.hvpdOnline] set ip='%s',reNewTimet=%d where cameraID='%s'" \
                   % (_hvpd[0], _hvpd[0], dictin["ip"], _timeSec, dictin["ip"], _timeSec, _hvpd[0])
            mssql.insert(_sql)
    except Exception, e:
        mylog.debug(str(e))
        return None
    socket.setdefaulttimeout(1)
    wtclib_mssql.http_get_cgi_msg2device(_dict_msg, dictin["ip"], "setting")

if __name__ == '__main__':

    mylog = wtclib_mssql.create_logging('SetupUdpserver.log')
    mylog.info("udp is running start")
    #_cur = get_a_mssql_cur_forever(mylog)
    _sql = "create table dbo.hvpdOnline(" \
           "cameraID char(24) primary key," \
           "ip char(24) not null," \
           "reNewTimet int default 0," \
           "reNewDate DATETIME default getdate());" \

    mssql = Mssql()
    mssql.insert(_sql)
    _udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    _udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    _udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    ADDR = ('', 9982)
    _udp_sock.bind(ADDR)

    udp_cnt = 0
    _udp_sock.settimeout(60)
    mylog.info(ADDR)
    while True:
        try:
            (data, addr) = _udp_sock.recvfrom(1024)
        except Exception, e:
            mylog.warning("udp receive "+str(e))
            #time.sleep(10)
            continue
            mylog.debug(data)
        _dict = udp_recv_is_json(data)
        if None != _dict:
            mylog.debug(data)
            info = udp_recv_data_process(_dict, mylog)

        msg = "nothing"
        _udp_sock.sendto(msg, addr)
