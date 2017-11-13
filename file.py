#-*- coding:utf-8 -*-
#######pyqt  文件载入对话框，文件保存对话框，打开文件夹对话框
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import tarfile
import gzip, os
from M2Crypto.EVP import Cipher
from M2Crypto import m2
from M2Crypto import util

ENCRYPT_OP = 1
DECRYPT_OP = 0

iv = '\0' * 16  # init not used for aes_128_ecb
PRIVATE_KEY = "hsylgwk-2012aaaa"


class MyWindow(QDialog,QWidget):
    def __init__(self,parent = None):
        super(MyWindow,self).__init__(parent)
        self.resize(400,150)
        self.mainlayout = QGridLayout(self)
        """
        self.loadFileButton = QPushButton()
        self.loadFileButton.setText(u"载入文件")
        self.mainlayout.addWidget(self.loadFileButton,0,0,1,1)
        self.loadFileLineEdit = QLineEdit()
        self.mainlayout.addWidget(self.loadFileLineEdit,0,1,1,4)
        self.loadFileButton.clicked.connect(self.loadFile)

        self.saveFileButton = QPushButton()
        self.saveFileButton.setText(u"保存文件")
        self.saveFileLineEdit = QLineEdit()
        self.mainlayout.addWidget(self.saveFileButton,1,0,1,1)
        self.mainlayout.addWidget(self.saveFileLineEdit,1,1,1,4)
        self.saveFileButton.clicked.connect(self.saveFile)

        self.openFileDirButton = QPushButton()
        self.openFileDirButton.setText(u"打开文件目录")
        self.mainlayout.addWidget(self.openFileDirButton,2,0,1,1)
        self.openFileDirButton.clicked.connect(self.openFileDirectory)
        """
        self.openFileDirButton = QPushButton()
        self.openFileDirButton.setText(u"打包压缩并加密文件夹")
        self.mainlayout.addWidget(self.openFileDirButton, 3, 0, 1, 1)
        self.openFileDirButton.clicked.connect(self.compress)
    """
    def loadFile(self):########载入file
        file_name = QFileDialog.getOpenFileName(self,"open file dialog","C:\Users\Administrator\Desktop","Txt files(*.txt)")
        ##"open file Dialog "文件对话框的标题，第二个是打开的默认路径，第三个是文件类型
        self.loadFileLineEdit.setText(file_name)

    def saveFile(self):
        self.file_path =  QFileDialog.getSaveFileName(self,'save file',"saveFile" ,"xj3dp files (*.xj3dp);;all files(*.*)") ####
        print self.file_path

    def openFileDirectory(self):
        import os
        os.popen("explorer.exe C:\Users\Administrator\Desktop")
    """
    def compress(self):
        path = QFileDialog.getExistingDirectory()
        print path
        #path +='/'
        tar_file_gzip(str(path))
        sys.exit()


def Encrypt(data):
    print "Enc len=",len(data)
    cipher = Cipher(alg='aes_128_ecb', key=PRIVATE_KEY, iv=iv, op=ENCRYPT_OP)
    buf = cipher.update(data)
    buf = buf + cipher.final()
    del cipher
    return buf
    """
    output = ''
    for i in buf:
        output += '%02X' % (ord(i))
    return output"""


def Decrypt(data):

    #data = util.h2b(data)
    print "Dec len=", len(data)
    cipher = Cipher(alg='aes_128_ecb', key=PRIVATE_KEY, iv=iv, op=DECRYPT_OP)
    buf = cipher.update(data)
    buf = buf + cipher.final()
    del cipher
    return buf
def tar_file_gzip(path):
    tar = tarfile.open("ttar.tar.gz", "w:gz")
    try:
        root, dir, files = os.walk(path)
    except Exception, e:
        print e
    for root, dir, files in os.walk(path):
        for file in files:
            fullpath = os.path.join(root, file)
            tar.add(fullpath)
    tar.close()
    aes_file("ttar.tar.gz")

def aes_file(filename):
    fd = open(filename, 'rb')
    fistat = os.stat(filename)
    lenthWr = 0
    fdout = open("update.bin", 'wb')
    fdD = open("update.tar.gz", 'wb')
    wrlen = 0
    """
    while fistat.st_size - lenthWr > 127:
        datai = fd.read(127)
        print "read len=", len(datai)
        datao = Encrypt(datai)
        print "after enc len=",len(datao)
        fdout.write(datao)
        decry = Decrypt(datao)
        print "after dec len=", len(decry)
        wrlen += len(decry)
        fdD.write(decry)
        lenthWr += 127;
        print lenthWr
        print "write = ",wrlen"""
    while fistat.st_size - lenthWr > 0:
        datai = fd.read(15)
        print "read len=", len(datai)
        datao = Encrypt(datai)
        fdout.write(datao)
        decry = Decrypt(datao)
        print "after dec len=", len(decry)
        wrlen += len(decry)
        fdD.write(decry)
        lenthWr += 15
        print lenthWr
        print "write = ", wrlen

    fd.close()
    fdD.close()
    fd.close()
app=QApplication(sys.argv)
window=MyWindow()
window.show()
app.exec_()
print app