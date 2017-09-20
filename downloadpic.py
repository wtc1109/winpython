#! /usr/bin/env python

import urllib, time

def report(done, block, size):
    print done,block,size
    print 100*done*block/size
print time.time()
try:
    f = urllib.urlopen("http://192.168.7.185/info/hub.c")
    print f.getcode()
except IOError,e:
    print e
    print "urlopen fail"
print time.time()
print "continue"
try:
    fd, info = urllib.urlretrieve("http://192.168.7.185/info/hub.c", "d:/123/1.c", reporthook=report)
    print fd
    print info
    print "********"
except IOError, e:
    print e
finally:
    urllib.urlcleanup()
    print "end"
print time.time()