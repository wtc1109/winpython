import socket
import time
host = "13"
port = 9981
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
addr1 = ("255.255.255.255", port)
#sock.bind(addr1)
while True:
    try:
        sock.sendto("asfhu", addr1)
    except Exception, e:
        print e
    time.sleep(5)