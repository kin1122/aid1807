from socket import *
import os,sys
import signal


def main():
    HOST = ''
    PORT = 8888
    ADDR = (HOST,PORT)

    s=socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(6)

    print('等待客户端连接．．．')

    while True:
        c,addr=s.accept()
        print('%s连接成功',addr)
        c.send('''\
++++++++++++++++++++++
|1.查看文件           |
|2.下载文件           |
|3.上传文件           |
++++++++++++++++++++++\
            '''.encode())
        data=c.recv(1024)
        if data.decode() == '1':
            Myftp.say()
        elif data.decode() == '2':
            Myftp.load()
        elif data.decode() == '3':
            Myftp.upload()
        else:
            c.send('您输入的信息不合法，请重新输入'.encode())



main()