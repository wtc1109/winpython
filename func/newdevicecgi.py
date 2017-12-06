#!/usr/bin/python
import sqlite3
import time
print "Content-type:text/html\n\n"
print """<html>
<head>
<meta content="text/html;charset=ISO-8869-1" http-equiv="content-type">
<meta http-equiv="refresh" content="2" />
<title>New Device</title>
</head>
<body>
<h1>New Devices in 30 min</h1>
<table>
	<tr>
<td  width="200"> MAC</td><td width="150">cameraID</td><td width="200">time</td><td width="200">CPUINFO</td>
</tr>"""

try:
    conn = sqlite3.connect("Producer.db")
    cur = conn.cursor()
except Exception, e:
    print "connect to DB err= "+str(e)
_timeNow = time.time()
cur.execute("select * from DeviceTable where time_int>%d"%int(_timeNow - 300*60))
_devices = cur.fetchall()
if None != _devices:
    _devs = sorted(_devices, key=lambda x:x[5], reverse=True)
    for dev in _devs:
        if dev[5] > (_timeNow-5*60):
            print "<tr><td>%s</td> <td>%s</td> <td bgcolor=red>%s</td> <td bgcolor=red>%s</td></tr>"%(dev[2], dev[3], dev[4], dev[0])
        else:
            print "<tr><td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td></tr>" % (dev[2], dev[3], dev[4], dev[0])
print """</table> </body> </html>"""



