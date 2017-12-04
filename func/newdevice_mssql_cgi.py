#!/usr/bin/python
import pymssql
import time
import wtclib_mssql
import datetime
def get_a_mssql_cur_forever():
    while True:
        (ret, err)=wtclib_mssql.get_a_mssql_cur_once("conf.ini")
        if None != ret:
            return ret
        else:
            print (err)
            time.sleep(20)
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
            cur.execute(sql)
            rows = cur.fetchall()
            cur.close()
            self.conn.close()
            return rows
        except Exception, e:
            print (str(e))
            return None
    def insert(self, sql):
        try:
            cur = self.__Connect()
            cur.execute(sql)
            cur.close()
            self.conn.commit()
            self.conn.close()
            return 0
        except Exception, e:
            print (str(e))
            return None

print "Content-type:text/html\n\n"
print """<html>
<head>
<meta content="text/html;charset=ISO-8869-1" http-equiv="content-type">
<meta http-equiv="refresh" content="3" />
<title>New Device</title>
</head>
<body>
<h1>New Devices in 30 min</h1>
<table>
	<tr>
<td  width="200"> MAC</td><td width="150">cameraID</td><td width="200">time</td><td width="200">CPUINFO</td>
</tr>"""

mssql = Mssql()
_timeNow = time.time()
print _timeNow
_sql = "select * from dbo.IPNC where EditFlag>dateadd(minute,-300,getdate())"
_devices = mssql.select(_sql)
print time.time()
#_devices = None
print "device all=%d"%len(_devices)
if None != _devices:
    _devs = sorted(_devices, key=lambda x:x[5], reverse=True)

    for dev in _devs:
        _macStr = "%06X" % dev[5]
        _mac = "00-1B-38-%s-%s-%s" % (_macStr[0:2], _macStr[2:4], _macStr[4:6])
        if dev[5] > (_timeNow-5*60):
            print "<tr><td>%s</td> <td>%s</td> <td bgcolor=red>%s</td> <td bgcolor=red>%s</td></tr>"%(_mac, dev[0], dev[13], dev[7])
        else:
            print "<tr><td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td></tr>" % (_mac, dev[0], dev[13], dev[7])
print """</table> </body> </html>"""



