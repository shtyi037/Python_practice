#UPD_client.py
from socket import *
import sys

HOST = sys.argv[1]
PORT = int(sys.argv[2])
ADDR = (HOST,PORT)
BUFFERSIZE = 1024

sockfd = socket(AF_INET,SOCK_DGRAM)

while True:
    data = input("消息>>")
    #輸入空格,客戶端退出
    if not data:
        break
    #發送消息給server
    sockfd.sendto(data.encode(),ADDR)
    data,addr = sockfd.recvfrom(BUFFERSIZE)
    print("server接收:",data.decode())

#關閉
sockfd.close()
