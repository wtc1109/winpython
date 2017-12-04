#coding=gbk
import os,sys

fi = open("123.txt", 'r')
str1 = fi.read()
str2 = "京AB12"
str3 = "京AB12"
_matchtime = []
for i in range(8):
    _matchtime.append(i+10)
print _matchtime.index(min(_matchtime))

#print cmp(str2,str3)
pre_similar_table = ['0DQ','8BRH',
                     'S53','2Z',
                     'T71','PRF',
                     'PRF','6G',
                     '4A']
for list1 in pre_similar_table:
    #print list1.index('D')
    print list1.find('D')
    print ('D'in list1)
print str1
for i in str1:
    print hex(ord(i))
for i in str2:
    print hex(ord(i))