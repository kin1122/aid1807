from socket import *
import sys,os
import signal
import time

#文件库路径
FILE_PATH="/home/tarena/ftp_file/"
HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST,PORT)

#将文件服务器功能卸载类中
class FtpServer(object):
    def __init__(self,connfd):
        self.connfd=connfd
    
    def do_list(self):
        #获取文件列表
        file_list=os.listdir(FILE_PATH)
        if not file_list:
            self.connfd.send('文件库为空'.encode())
        else:
            self.connfd.send(b'OK')
            time.sleep(0.1)
        files=''
        for file in file_list:
            if file[0] != '.' and os.path.isfile(FILE_PATH+file):
                files= files + file + '#'
        self.connfd.send(files.encode())
    def do_get(self,filename):
        try:
            fd=open(FILE_PATH+filename,'rb')
        except:
            self.connfd.send('文件不存在'.encode())
            return
        self.connfd.send(b'OK')
        time.sleep(0.1)
        while  True:
            data=fd.read(1024)
            if not data:
                time.sleep(0.1)
                self.connfd.send(b'##')
                break
            self.connfd.send(data)
        print('文件发送完毕')  




#创建套接字，接收客户端连接，创建新的进程
def main():
    sockfd=socket()
    sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    sockfd.bind(ADDR)
    sockfd.listen(6)
    print('等待客户端连接．．．')
    #处理子进程退出
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    print('监听套接字端口8888..')
    while True:
        try:
            connfd,addr=sockfd.accept()
        except KeyboardInterrupt:
            sockfd.close()
            sys.exit('服务器异常')
        except Exception as e:
            print('服务器异常',e)
            continue
        print('已连接客户端:',addr)

        #创建子进程
        pid = os.fork()
        if pid == 0:
            sockfd.close()
            ftp =FtpServer(connfd)
            #判断客户端请求
            while True:
                data=connfd.recv(1024).decode()
                print(data)
                if not data or data[0] == 'Q':
                    connfd.close()
                    sys.exit('客户端退出')
                elif data[0] == 'L':
                    ftp.do_list()
                elif data[0] == 'G':
                    filename=data[1:]
                    ftp.do_get(filename)
            



        else:
            connfd.close()
            continue


if __name__=='__main__':
    main()