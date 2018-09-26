from socket import *

# 本机IP
# 176.140.8.213



sockfd=socket()
sockfd.connect(('176.140.8.213',8888))
while True:
    
    data=input("输入要发送的信息")
    if not data:
        break
    sockfd.send(data.encode())
    n=sockfd.recv(1024)
    print(n.decode())
sockfd.close()