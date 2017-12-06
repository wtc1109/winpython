import os, json
import crypto
import time
import datetime
import math
import struct
import difflib
import zipfile
import tarfile
en = zipfile.is_zipfile("env.zip")
zip0 = zipfile.ZipFile("env.zip",'r')
info0 = zip0.namelist()

en1 = zipfile.is_zipfile("env.rar")
en2 = tarfile.is_tarfile("ttar.tar.gz")
tar2 = tarfile.open("ttar.tar.gz")
info2 = tar2.getmembers()
print time.asctime()
now = datetime.datetime.now()
stamp = datetime.datetime.fromtimestamp(time.time()-3600)
print now < stamp
print str(now)
hex_str = "1a2b3c"
rgb = "R:0,G:80,B:0"
rgb3="R:80,G:80,B:10"
match = difflib.SequenceMatcher(None,rgb, rgb3)
fl1 = match.ratio()
rgb1=rgb.split(',')
rgb2={}
for rg in rgb1:
    rg2 = rg.split(':')
    rgb2.update({rg2[0]:rg2[1]})

dic2=json.dumps(rgb)
xy = [1,2,5,4,3]
_pos = [None,None,None]
_pos[0] = "sef"
_m = xy.pop(xy.index(max(xy)))
_int_1 = int(hex_str,16)
_int_val = hex_str.encode("ascii")
#(val,) = struct.unpack("<L",bytes(_int_val))
print time.gmtime(1509720398)
print os.environ
dic = {1:100}
jstr = json.dumps(dic)
fl = time.time()
str1 = min("123456789", "123456788")
(fraction1, inter1) = math.modf(fl)
sec = int(time.time())
list1 = []
datetime1 = time.localtime()
list1.append("1")
list1[0] = 1
list1.append("0")
list1.append("0")
list1.append("1")
list2 = []
list2.append(time.time())
time.sleep(0.2)
list2.append(time.time())
time.sleep(0.2)
list2.append(time.time())
time.sleep(0.2)
list2.append(time.time())
sec_str = "%d_%d"%(sec, int(1000*fraction1))
print jstr
import binascii
connect = "123;456;79\r\n13;46;sdf\r\n"
print binascii.b2a_hex(connect)
list1 = connect.split("\r\n")
str1 = (list1[i] for i in range(2))
#print '%s,%s'%(list1[i] for i in range(2))
timenow1 = datetime.datetime.now()
timet = time.mktime(timenow1.timetuple())
datetime1 = time.localtime()
str1 = "sfowef\r\n"
str2 = str1.rstrip("\r\n")
tp = type(jstr)
print tp
key1 = "hsylgwk-2012aaaa"
instr = "1234567890"
timestr = str(time.time())
print time.time(),"len=",len(timestr)
