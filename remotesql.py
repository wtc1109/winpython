import MySQLdb

try:
    conn = MySQLdb.connect(host="192.168.7.19", user="root", passwd="123456", db="AlgReturndb2", port=3306)
    conn.autocommit(1)
    cur = conn.cursor()
except Exception, e:
    print e
    conn = MySQLdb.connect(host="192.168.7.19", user="root", passwd="123456")
    conn.autocommit(1)
    cur = conn.cursor()
    cur.execute("create database AlgReturndb2")
    cur.execute("use AlgReturndb2")
print "er"