from socket import *
import os,sys
import signal
import time

#基本文件操作功能
class FtpClient(object):
    def __init__(self,sockfd):
        self.sockfd=sockfd

    def do_list(self):
        self.sockfd.send(b'L')
        #等待回复
        data=self.sockfd.recv(1024).decode()
        if data == 'OK':
            data=self.sockfd.recv(4096).decode()
            files=data.split('#')
            for file in files:
                print(file)
            print('文件列表展示完毕\n')
        else:
            #打印请求失败的原因
            print(data)
    def do_get(self,filename):
        self.sockfd.send(('G'+filename).encode())
        data=self.sockfd.recv(1024).decode()
        if data == 'OK':
            fd=open(filename,'wb')
            while  True:
                data=self.sockfd.recv(1024)
                if data ==b'##':
                    break
                fd.write(data)
            fd.close()
            print('%s下载完毕\n' % filename)

        else:
            print(data)

    def do_quit(self):
        print('-------------')
        self.sockfd.send(b'Q')

#
def main():
    if len(sys.argv)<3:
        print("argv is error")
        return
    HOST=sys.argv[1]
    PORT=int(sys.argv[2])
    ADDR=(HOST,PORT)

    sockfd=socket()
    try:
        sockfd.connect(ADDR)
    except:
        print('连接服务器异常')
        return

    ftp=FtpClient(sockfd)#功能类对象
    while True:
        print('''\
++++++++++++++++++++++
|list-->查看文件      |
|load-->下载文件      |
|upload-->上传文件    |
++++++++++++++++++++++''')
        cmd=input('请输入命令>>>')
        if cmd.strip() == 'list':
            ftp.do_list()
        elif cmd[:3] == 'get':
            filename=cmd.split(' ')[-1]
            print(filename)
            ftp.do_get(filename)
        elif cmd == 'quit':
            print('----------------')
            ftp.do_quit()
            sys.exit('谢谢使用')
            

        else:
            print("请输入正确命令")
            continue


if __name__=='__main__':
    main()
