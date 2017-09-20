#! /usr/bin/env python

import urllib

def report(done, block, size):
    print done,block,size
    print 100*done*block/size

f = urllib.urlopen("http://192.168.7.185/info/hub1.c")
print f.getcode()
try:
    fd, info = urllib.urlretrieve("http://192.168.7.185/info/hub.c", "/tmp/1.c", reporthook=report)
    print fd
    print info
    print "********"
finally:
    urllib.urlcleanup()
