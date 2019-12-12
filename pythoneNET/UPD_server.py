#UDP_server.py
from socket import * 
import sys 
from time import ctime


HOST = sys.argv[1]
PORT = int(sys.argv[2])
ADDR = (HOST,PORT)
BUFFERSIZE = 5


sockfd = socket(AF_INET,SOCK_DGRAM)
sockfd.bind(ADDR)

#收發
while True:
    data,addr = sockfd.recvfrom(BUFFERSIZE)
    print("recv from ",addr,':',data.decode())
    sockfd.sendto\
    (("在　%s 接受到你的消息"%ctime()).encode(),addr)

#關閉
sockfd.close()
