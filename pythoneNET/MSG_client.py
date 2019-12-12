#練習作業
#寫一個聊天室
#當一個用戶進入聊天室，發消息，聊天室內所有用戶都能收到消息
#每當有用戶進入或者退出群聊時，其他成員能夠收到進入和退出的信息
#消息收發時，不讓自己收到，並且有一定格式
# 張三發送了個 hello   > hello   
# 其他成員顯示為張三 say ： hello
#(進入聊天室就要確定下自己的姓名)
#
#管理員喊話：服務器發送消息所有成員都能收到


#MSG_client.py

from socket import *
import select
import sys
import time
import threading 

#接收server傳送的訊息
def broadRece(conn):
    count = 0
    if count ==0:
        print("進程開始")
        count += 1
    # if name != 'NONAME':
    while True: #為了持續的接收訊息    
        Ser_data = conn.recv(1024)#接收Server傳過來的訊息
        print(Ser_data.decode())#\n為跳行
        # print("\nServer>>",Ser_data.decode())#\n為跳行

#發給server的訊息
def broadSend(conn):
        while True: #為了維持持續的發送 
            data = input(">>>")
            conn.sendall(data.encode())#送出資料


def main():
    if len(sys.argv) !=3:
        print("argv is Error!!!!")
        sys.exit(1)
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST,PORT)
    BUFFERSIZE = 1024
    #創建網絡連接
    L_Client = socket()
    L_Client.connect(ADDR)#與伺服器連接
    name = 'NONAME'
    #thread_send = threading.Thread(target=broadSend, args=(L_Client, )) #發
    thread_recv = threading.Thread(target=broadRece, args=(L_Client, )) #收
    thread_recv.setDaemon(True)#子線程隨主線​​程的結束
    thread_recv.start()
    while True:
        #輸入使用者名稱
        if name is 'NONAME':
            New_name = input("您的名稱為:")
            Uname = 'name '+New_name
            L_Client.sendall(Uname.encode()) #傳送使用者名稱給Server(只有一次)
            name = New_name
        else:
            #print(name,end='') #顯示自己的名字
            data = input(">")
            if data == 'exit':
                L_Client.close()
                sys.exit()
            L_Client.sendall(data.encode())#發出資料
            # Ser_data = L_Client.recv(BUFFERSIZE)#接收Server傳過來的訊息
            # print("Server傳送的訊息為:",Ser_data.decode())
    # L_Client.close()

if __name__ == '__main__':
    main()
