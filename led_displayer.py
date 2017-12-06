import ConfigParser
import Queue
import json
import os
import socket
import threading
import time

import MySQLdb

from func import wtclib

ROOT_DIR=""

global mylog


THREAD_NUM = 1 #how many threads
gQueues = []
for i in range(THREAD_NUM):
    Info_queue = Queue.Queue(maxsize=5)
    gQueues.append(Info_queue)
gQueue_ret = Queue.Queue(maxsize=20)


def analyze_udp_info2dict(msg):
    ret = msg.find('LEDID')
    if 0 != ret:
        return None
    #msg.rstrip("\r\n")
    ret = msg.find(':')
    msg2 = msg[ret+1:].rstrip("\r\n")
    list1 =msg2.split(' ')
    return list1

def make_sql_udp_info_str(info, Errflag):
    val = "'%s'," % info[0]
    for i in range(1, 4):
        val += "%s, " % info[i]
    for i in range(4, 11):
        val += "'%s', " % info[i]
    val += info[11] + ','
    for i in range(12, 16):
        val += "'%s', " % info[i]
    val += "%d, %d, " % (info[16], Errflag)

    str1 = "(LEDID , width, height, unitSum, distanceP2P, color, definition, minPix, productName, " \
           "HardwareVersion, softwareVersion, currentSerialNo, MAC, refresh, systemFlag, IPaddress," \
                       "port, ErrorFlag, time) " \
           "values(" + val + " now())"
    return str1

def sql_insert_into_table(info, table, cur, Errflag):
    str1 = "insert into "+ table + make_sql_udp_info_str(info, Errflag)
    try:
        cur.execute(str1)
    except Exception, e:
        mylog.error(str1)
        mylog.error(str(e))
    return
def sql_replace_into_table(info, table, cur):
    str1 = "replace into "+ table + make_sql_udp_info_str(info) + "where LEDID='%s'"%info[0]
    try:
        cur.execute(str1)
    except Exception, e:
        mylog.error(str1)
        mylog.error(str(e))
    return
def update_udp_into2sql(info):
    if "00006899999" == info[0]:
        sql_insert_into_table(info, "LedDisplayerUdpErrorInfo", cur)
        return
    a1 = cur.execute("select * from LedDisplayerUdpInfo where LEDID='" + info[0] + "'")
    if a1 > 1:
        many_prodc = cur.fetchmany(a1)
        for prod in many_prodc:
            cur.execute("insert into LedDisplayerUdpErrorInfo select * from LedDisplayerUdpInfo where id=%d"%prod[0])
            #cur.execute("delete from LedDisplayerUdpInfo where id=%d"%prod[0])
        return


    if 0 == a1:
        a1 = cur.execute("select * from LedDisplayerUdpInfo where MAC='" + info[12] + "'")
        if 0 == a1:
            sql_insert_into_table(info, "LedDisplayerUdpInfo", cur, 0)
        else:
            many_prodc = cur.fetchmany(a1)
            for prod in many_prodc:
                cur.execute(
                    "insert into LedDisplayerUdpErrorInfo select * from LedDisplayerUdpInfo where id=%d" % prod[0])
            sql_insert_into_table(info, "LedDisplayerUdpErrorInfo", cur, 1)
    else:
        a1 = cur.execute("select * from LedDisplayerUdpInfo where MAC='" + info[12] + "'")
        if 0 == a1:#different MAC, so error
            sql_insert_into_table(info, "LedDisplayerUdpInfo", cur, 1)
        else:
            cur.execute("delete from LedDisplayerUdpInfo where LEDID='%s'"%info[0])
            sql_insert_into_table(info, "LedDisplayerUdpInfo", cur, 0)

    return

class led_displayer_udp_server(threading.Thread):
    def __init__(self):
        global ROOT_DIR
        self.__cur = get_a_sql_cur()
        self.__logger = wtclib.create_logging(ROOT_DIR + '/prog/log/leddisplog/udpserver.log')
        threading.Thread.__init__(self)
    def run(self):
        _udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ADDR = ('', 5266)
        _udp_sock.bind(ADDR)
        start_time = time.time()
        udp_cnt = 0
        while True:
            (data, addr) = _udp_sock.recvfrom(1024)
            info = []
            info = analyze_udp_info2dict(data)
            if None != info:
                info.append(addr[0])
                info.append(addr[1])
                if len(info) > 16:
                    update_udp_into2sql(info)
            msg = "nothing"
            _udp_sock.sendto(msg, addr)
            udp_cnt += 1
            if time.time() - start_time > 60:
                start_time = time.time()
                self.__logger.info("%d udp broadcast in 60sec"%udp_cnt)
                udp_cnt = 0

def get_count_carport_msg(ledsql, cur):
    msg = "LEDREGIONSDISPLAY %d 1 1 "%ledsql[12]
    _conf = cur.execute("select * from ScreenConfigTable where ScreenSn=%s"%ledsql[1])
    _ScreenConfig = cur.fetchmany(_conf)[0]
    msg += "%s %s %s "%(_ScreenConfig[2], _ScreenConfig[3], _ScreenConfig[4])
    localtimeN = time.localtime()
    for i in range(int(_ScreenConfig[4])):
        _regionConf = cur.execute("select * from ScreenRegionConfigTable where RegionSn=%s"%_ScreenConfig[5+i])
        if 0 == _regionConf:
            return None
        _ScreenRegionConf = cur.fetchmany(_regionConf)[0]
        msg += "%d %d %d %d %d %d %d "%(_ScreenRegionConf[1], _ScreenRegionConf[2], _ScreenRegionConf[3], _ScreenRegionConf[4],
                              _ScreenRegionConf[5], _ScreenRegionConf[6], _ScreenRegionConf[7])
        if "\"%c\"" == _ScreenRegionConf[8]:
            """
            a1 = cur.fetchmany(cur.execute("select count(*) from SpaceStatusTable where CarportStatus=0 and Spaceid "
                        "in (select Spaceid from Space2LedTable where RegionSn in "
                        "(select RegionSn from ScreenRegionConfigTable as Led where RegionSn=%d))" % (
                        _ScreenConfig[5 + i])))[0]"""
            a1 = cur.fetchmany(cur.execute("select count(*) from SpaceStatusTable where CarportStatus=0 and Spaceid in"
                                           " (select Spaceid from Space2LedTable where RegionSn=%d)"%_ScreenConfig[5 + i]))[0]
            msg += "%d\t"%(a1[0])
        elif "\"%h\"" == _ScreenRegionConf[8]:
            msg += "%d\t"%(localtimeN.tm_hour)
        elif "\"%m\"" == _ScreenRegionConf[8]:
            msg += "%d\t" % (localtimeN.tm_min)
        elif "\"%w\"" == _ScreenRegionConf[8]:
            msg += "%d\t" % (localtimeN.tm_wday+1)

        elif "\"%Y\"" == _ScreenRegionConf[8]:
            msg += "%d\t" % (localtimeN.tm_year)
        elif "\"%M\"" == _ScreenRegionConf[8]:
            msg += "%d\t" % (localtimeN.tm_mon)
        elif "\"%D\"" == _ScreenRegionConf[8]:
            msg += "%d\t" % (localtimeN.tm_mday)
        else:
            msg1 = _ScreenRegionConf[8].strip("\"")
            msg += msg1 + '\t'
    _xor_val = 0;
    for datai in msg:
        _xor_val = _xor_val ^ ord(datai)
    msg += "%02X\r\n"%_xor_val
    return msg


class led_displayer_tcp_client(threading.Thread):
    def __init__(self, num):
        global ROOT_DIR
        self.__cur = get_a_sql_cur()
        self.__id = num
        self.__logger = wtclib.create_logging(ROOT_DIR + '/prog/log/leddisplog/tcpclient%d.log' % num)
        threading.Thread.__init__(self)
    def run(self):
        global gQueues, gQueue_ret

        while True:
            _recv_json = gQueues[self.__id].get(block=True)
            #start_time = time.time()
            _recv_dict = json.loads(_recv_json)
            a1 = self.__cur.execute("select * from LedDisplayerUdpInfo where LEDID='" + _recv_dict['LEDID'] + "'")
            if 0 == a1:
                _dic1 = {"ret":0,"err":"no sql info", "id":self.__id}
            elif a1 > 1:
                _dic1 = {"ret": 0, "err": "too many LEDID", "id":self.__id}

            else:
                ledsql = self.__cur.fetchmany(a1)[0]
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                address = (ledsql[16], 5813)
                try:
                    sock.connect(address)
                    msg = get_count_carport_msg(ledsql, self.__cur)
                    if None != msg:
                        sock.send(msg)
                        self.__logger.debug(msg)
                        _dic1 = {"ret": 1, "id":self.__id}
                    else:
                        _dic1 = {"ret": 0, "id": self.__id, "err":"msg None"}
                except Exception, e:
                    _dic1 = {"ret":0, "err":str(e), "id":self.__id}
                    self.__logger.info("LEDID:%s,ip=%s"%(ledsql[1], ledsql[16]))
                    self.__logger.info(str(e))
                try:
                    sock.close()
                except Exception, e:
                    self.__logger.info("socket close "+str(e))
            _recv_dict.update(_dic1)
            gQueue_ret.put(json.dumps(_recv_dict))
            #print "use sec ", time.time()-start_time, self.__id


def make_some_virtualLeds_indb(cur):
    for i in range(123456, 123468):
        cur.execute("insert into LedDisplayerUdpInfo(LEDID, IPaddress) values('%d', '192.168.7.18')"%i)
    #for i in range(123556, 123560):
    #    cur.execute("insert into LedDisplayerUdpInfo(LEDID, IPaddress) values('%d', '192.168.8.18')"%i)

def get_a_sql_cur():
    cf = ConfigParser.ConfigParser()
    try:
        cf.read("conf.conf")
    except Exception, e:
        mylog.error(str(e))
        return None
    secs = cf.sections()
    try:
        opts = cf.options("db")
    except Exception, e:
        mylog.error(str(e)+' db')
        return None
    try:
        DB_host = cf.get("db", "location")
        DB_user = cf.get("db", "user_name")
        DB_passwd = cf.get("db", "user_passwd")
        DB_name = cf.get("db", "name")
    except Exception, e:
        mylog.error(str(e)+' get db')
        return None
    while True:
        try:
            conn = MySQLdb.connect(host=DB_host, user=DB_user, passwd=DB_passwd, db=DB_name)
            conn.autocommit(1)
            cur = conn.cursor()
            break
        except:
            time.sleep(20)
            mylog.warn("Can't connect to MySQL")
    cur.execute("use " + DB_name)
    return cur
def create_qld_db(cur):
    try:
        cur.execute("create table if not exists LedDisplayerUdpInfo("
                    "id int not null auto_increment primary key,"  # 0  
                    "LEDID char(16) , "         #1
                    "width smallint,"               #2
                    "height smallint,"              #3
                    "unitSum tinyint,"              #4
                    "distanceP2P char(8),"          #5
                    "color char(16),"               #6
                    "definition char(16),"          #7
                    "minPix char(8),"               #8
                    "productName char(16),"         #9
                    "HardwareVersion char(16),"     #10
                    "softwareVersion char(16),"     #11
                    "currentSerialNo smallint,"     #12
                    "MAC char(24),"                 #13
                    "refresh char(4),"              #14
                    "systemFlag char(8),"           #15
                    "IPaddress char(24),"           #16
                    "port int,"                     #17
                    "ErrorFlag tinyint default 0,"  #18
                    "time DATETIME"  # 1            
                    ")engine=memory")  # 17
    except Exception, e:
        print "create table LedDisplayerUdpInfo", e
        pass
    #make_some_virtualLeds_indb(cur)
    try:
        cur.execute("create table if not exists LedDisplayerUdpErrorInfo("
                    "id int not null auto_increment primary key,"
                    "LEDID char(16),"  # 0
                    "width smallint,"
                    "height smallint,"
                    "unitSum tinyint,"
                    "distanceP2P char(8),"
                    "color char(16),"
                    "definition char(16),"
                    "minPix char(8),"
                    "productName char(16),"
                    "HardwareVersion char(16),"
                    "softwareVersion char(16),"
                    "currentSerialNo smallint,"
                    "MAC char(24),"
                    "refresh char(4),"
                    "systemFlag char(8),"
                    "IPaddress char(16), "
                    "port int,"
                    "ErrorFlag tinyint default 0,"
                    "time DATETIME"  # 1
                    ")engine=memory")  # 17
    except Exception, e:
        print "create table LedDisplayerUdpErrorInfo", e
        pass

def get_root_dir_config():
    cf = ConfigParser.ConfigParser()
    try:
        cf.read("conf.conf")
    except Exception, e:
        mylog.error(str(e))
        return None
    secs = cf.sections()
    try:
        opts = cf.options("file_save")
    except Exception, e:
        mylog.error(str(e) + ' file_save')
        return None
    try:
        dirs = cf.get("file_save", "root_dir")
        return dirs
    except Exception, e:
        mylog.error(str(e) + ' get file_save')
        return None

def check_screen_connect_table(cur):
    try:
        cur.execute("create table if not exists ScreenConnectTable("
                    "ScreenSn char(16)not null primary key,"
                    "ScreenName char(16))engine=memory")
    except Exception, e:
        pass
def update_screen_connect_sql(path, cur):
    filei = open(path, 'r')
    try:
        check_screen_connect_table(cur)
        while True:
            line = filei.readline()
            if line:
                line1 = line.rstrip('\r\n')
                list1 = line1.split(';')
                if 3 != len(list1):
                    continue
                cur.execute("insert into ScreenConnectTable(ScreenSn, ScreenName) "
                            "values('%s', '%s')ON DUPLICATE KEY UPDATE ScreenName='%s'"
                            %(list1[1], list1[2], list1[2]))
            else:
                break
    finally:
        filei.close()
    return

def check_screen_config_table(cur):
    try:
        cur.execute("create table if not exists ScreenConfigTable("
                    "ScreenSn char(16)not null primary key,"
                    "CtrlMode int,"
                    "Weight int, "
                    "height int,"
                    "AllRegion int,"
                    "Region1 int, "
                    "Region2 int,"
                    "Region3 int,"
                    "Region4 int,"
                    "Region5 int,"
                    "Region6 int,"
                    "Region7 int,"
                    "Region8 int"
                    ")engine=memory")
    except Exception, e:
        pass
    try:
        cur.execute("create table if not exists ScreenRegionConfigTable("
                    "RegionSn int not null primary key,"
                    "TopLeftX int,"
                    "TopLeftY int, "
                    "BottomRightX int,"
                    "BottomRightY int,"
                    "Action int,"
                    "Font int, "
                    "Color int,"
                    "Display char(8)"
                    ")engine=memory")
    except Exception, e:
        pass


def update_screen_config(path, cur):
    filei = open(path, 'r')
    try:
        check_screen_config_table(cur)
        while True:
            line = filei.readline()
            if line:
                line1 = line.rstrip('\r\n')
                list1 = line1.split(';')

                cur.execute("insert into ScreenConfigTable(ScreenSn, CtrlMode, Weight, height, AllRegion) "
                            "values('%s', %s, %s, %s, %s)ON DUPLICATE KEY UPDATE CtrlMode=%s, "
                            "Weight=%s, height=%s, AllRegion=%s"
                            ""%(list1[0], list1[1], list1[2], list1[3], list1[4], \
                                list1[1], list1[2], list1[3], list1[4]))
                for i in range(int(list1[4])):
                    _region = list1[5+i].split(',')
                    cur.execute("update ScreenConfigTable set Region%d = %s"
                                " where ScreenSn='%s'"
                                "" % (i+1, _region[8], list1[0]))
                for _RegionInfo in list1[5:]:
                    if 0 == len(_RegionInfo):
                        break
                    _region = _RegionInfo.split(',')
                    cur.execute("insert into ScreenRegionConfigTable(TopLeftX, TopLeftY, BottomRightX, "
                            "BottomRightY, Action, Font, Color, Display, RegionSn) "
                            "values(%s, %s, %s, %s, %s, %s, %s, '%s', %s)ON DUPLICATE KEY UPDATE "
                            "TopLeftX=%s, TopLeftY=%s, BottomRightX=%s, BottomRightY=%s,"
                            "Action=%s, Font=%s, Color=%s, Display=%s"% (_region[0], _region[1], _region[2], _region[3], _region[4], _region[5], _region[6],
                                  _region[7], _region[8], _region[0], _region[1], _region[2], _region[3], _region[4],
                                  _region[5], _region[6],_region[7] ))
            else:
                break
    finally:
        filei.close()
    return
def update_screen2_config(path, cur):
    filei = open(path, 'r')
    try:
        check_screen_config_table(cur)
        while True:
            line = filei.readline()
            if line:
                line1 = line.rstrip('\r\n')
                list1 = line1.split(';')

                cur.execute("insert into ScreenConfigTable(ScreenSn, CtrlMode, Weight, height, AllRegion) "
                            "values('%s', %s, %s, %s, %s)ON DUPLICATE KEY UPDATE CtrlMode=%s, "
                            "Weight=%s, height=%s, AllRegion=%s"
                            ""%(list1[0], list1[2], list1[3], list1[4], list1[5],\
                                list1[2], list1[3], list1[4], list1[5]))
                for i in range(int(list1[5])):
                    _region = list1[6+i].split(',')
                    cur.execute("update ScreenConfigTable set Region%d = %s"
                                " where ScreenSn='%s'"
                                "" % (i+1, _region[8], list1[0]))
                for _RegionInfo in list1[6:]:
                    if 0 == len(_RegionInfo):
                        break
                    _region = _RegionInfo.split(',')
                    cur.execute("insert into ScreenRegionConfigTable(TopLeftX, TopLeftY, BottomRightX, "
                            "BottomRightY, Action, Font, Color, Display, RegionSn) "
                            "values(%s, %s, %s, %s, %s, %s, %s, '%s', %s)ON DUPLICATE KEY UPDATE "
                            "TopLeftX=%s, TopLeftY=%s, BottomRightX=%s, BottomRightY=%s,"
                            "Action=%s, Font=%s, Color=%s, Display='%s'"% (_region[0], _region[1], _region[2], _region[3], _region[4], _region[5], _region[6],
                                  _region[7], _region[8], _region[0], _region[1], _region[2], _region[3], _region[4],
                                  _region[5], _region[6],_region[7] ))
            else:
                break
    finally:
        filei.close()
    return

def check_region_config_table(cur):
    try:
        cur.execute("create table if not exists SpaceStatusTable("
                    "Spaceid char(32) not null primary key,"
                    "HVPDsn char(32), "
                    "Carport int,"
                    "CarportStatus int)engine=memory")
        cur.execute("drop table if exists Space2LedTable")
        cur.execute("create table Space2LedTable("
                    "id int not null auto_increment primary key,"
                    "Spaceid char(32), "
                    "RegionSn int)engine=memory")
    except Exception, e:
        pass

def update_region_config(path, cur):
    filei = open(path, 'r')
    try:
        check_region_config_table(cur)
        while True:
            line = filei.readline()
            if line:
                line1 = line.rstrip('\r\n')
                list1 = line1.split(';')
                cur.execute("insert into SpaceStatusTable(Spaceid, HVPDsn, Carport, CarportStatus) "
                            "values('%s', '%s', %s, 0)ON DUPLICATE KEY UPDATE HVPDsn='%s', Carport=%s"
                            % (list1[1]+list1[2], list1[1], list1[2], list1[1], list1[2]))
                cur.execute("insert into Space2LedTable(Spaceid, RegionSn) "
                            "values('%s', %s)"
                            % (list1[1] + list1[2], list1[0]))
            else:
                break
    finally:
        filei.close()
    return


def update_reserved_parking(path, cur):
    filei = open(path, 'r')
    try:
        cur.execute("update RegionConfigTable set CarportStatus=0 where CarportStatus=2")
        while True:
            line = filei.readline()

            if line:
                line1 = line.rstrip('\r\n')
                list1 = line1.split(';')
                cur.execute("update RegionConfigTable set CarportStatus=2 where id='%s'"%(list1[0]+list1[1]))
            else:
                break
    finally:
        filei.close()
    return


def renew_screen_info_sql(cur):
    global ROOT_DIR
    path = ROOT_DIR+"/prog/conf/"
    while not os.path.isdir(path):
        time.sleep(120)
    (snpath, dirs, filenames), = os.walk(path)
    print snpath
    for files in filenames:
        if 0 == files.find("HVCS_region_config"):
            update_region_config(path + files, cur)
            break
    for files in filenames:
        if 0 == files.find("HVCS_screen_connect"):
            update_screen_connect_sql(path+files, cur)
            continue
        if 0 == files.find("HVCS_screen_config"):
            update_screen_config(path+files, cur)
            continue
        if 0 == files.find("HVCS_screen2_config"):
            update_screen2_config(path+files, cur)
            continue
        if 0 == files.find("HVCS_reserved_parking"):
            update_reserved_parking(path+files, cur)
            continue
    return


if __name__ == '__main__':
    global ROOT_DIR
    ROOT_DIR = get_root_dir_config().rstrip("/")

    if not os.path.isdir(ROOT_DIR+"/prog/log/leddisplog"):
        try:
            os.mkdir(ROOT_DIR+"/prog/log/leddisplog")
        except Exception, e:
            print e
            os._exit()
    mylog = wtclib.create_logging(ROOT_DIR + "/prog/log/leddisplog/ledplayer.log")
    mylog.info("start")
    cur = get_a_sql_cur()
    create_qld_db(cur)
    _ConfChangeTime = os.stat(ROOT_DIR+"/prog/conf/").st_ctime
    renew_screen_info_sql(cur)
    if None == cur:
        mylog.error("connect to db fail")
        os._exit()
    thread = led_displayer_udp_server()
    thread.start()
    """"""
    #time.sleep(25)
    thread_idles = THREAD_NUM

    gThread_using_flag = []
    threads = []
    for i in range(THREAD_NUM):
        flag = 1
        gThread_using_flag.append(flag)
        thread = led_displayer_tcp_client(i)
        thread.start()
        time.sleep(0.1)
        threads.append(thread)
    while True:
        leds = cur.execute("select * from LedDisplayerUdpInfo")
        if 0 == leds:
            time.sleep(5)
            continue
        else:
            break
    _ConfDelay = 20
    while True:
        """ Auto renew Config ini files, delay 20times, near 60sec"""
        _ConfTime = os.stat(ROOT_DIR+"/prog/conf/").st_ctime
        if _ConfChangeTime != _ConfTime:
            _ConfDelay -= 1
            if _ConfDelay <= 0:
                _ConfChangeTime = os.stat(ROOT_DIR+"/prog/conf/").st_ctime
                _ConfDelay = 20
                renew_screen_info_sql(cur)

        start_time = time.time()
        leds = cur.execute("select * from LedDisplayerUdpInfo")
        ledsinfo = cur.fetchmany(leds)
        for led in ledsinfo:
            if 0 != led[18]:  #ErrorFlag
                mylog.warning(led[1]+" ErrorFlag=%d"%led[18])
                continue
            if 0 == cur.execute("select ScreenSn from ScreenConnectTable where ScreenSn='%s'"%led[1]):#not for connect ctrl
                continue

            try:
                refresh_time = time.mktime(led[19].timetuple())
            except:
                continue
            if start_time - refresh_time > 60:
                continue
            _dic = {"LEDID":led[1]}
            for i in range(THREAD_NUM):
                if 0 != gThread_using_flag[i]:
                    gQueues[i].put_nowait(json.dumps(_dic))
                    gThread_using_flag[i] = 0
                    i = THREAD_NUM+1
                    break
            if i > THREAD_NUM:
                continue
            else:
                rec_json = gQueue_ret.get(block=True)
                gThread_using_flag[json.loads(rec_json)["id"]] = 1
        timeused = time.time() - start_time
        print "process %d leddisplayer in %f second"%(leds, timeused)
        if timeused < 3:
            time.sleep(3-timeused)
        Cur_qsize = gQueue_ret.qsize()
        for i in range(Cur_qsize):
            rec_json = gQueue_ret.get(block=True)
            gThread_using_flag[json.loads(rec_json)["id"]] = 1