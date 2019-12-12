#ftp_client.py
from socket import * 
import sys 
import time

class FtpClient(object):
    def __init__(self,sockfd):
        self.sockfd = sockfd

    def do_list(self):
        self.sockfd.send(b"L") #發送請求類型
        #接收服務器確認 OK 或 FALL
        data = self.sockfd.recv(1024).decode()
        if data == 'OK':
            #成功,循環接收server回傳過來的文件名
            while True:
                data = self.sockfd.recv(1024).decode()
                if data == '##': #此為server端告知結束的訊息
                    break
                print(data)
            print("文件列表展示完畢")
            return
        else:
            #失敗
            print("文件列表請求失敗")
            return

    def do_get(self,filename):
        self.sockfd.send(("G " + filename).encode())
        #接收服務器確認 OK 或 FALL
        data = self.sockfd.recv(1024).decode()
        if data == 'OK':
            fd = open(filename,'w')
            while True:
                #收到server端發送的文字,寫入文件中
                data = self.sockfd.recv(1024).decode()
                if data == '##':
                #收到##則結束
                    break
                fd.write(data)
            fd.close()
            print('%s 下載完成'%filename)
            return
        else:
            print("下載文件失敗")
            return

    def do_put(self,filename):
        try:
            fd = open(filename,'rb')
        except:
            print("上傳的文件失敗")
            return 
        self.sockfd.send(("P " + filename).encode())
        #接收服務器確認 OK 或 FALL
        data = self.sockfd.recv(1024).decode()
        if data == 'OK':
            for line in fd:
                self.sockfd.send(line)
            fd.close()
            time.sleep(0.1)
            self.sockfd.send(b"##")
            print("上傳文件　%s　完成"%filename)
            return 
        else:
            print("上傳文件失敗")
            return

    def do_quit(self):
        self.sockfd.send(b"Q")

def main():
    #取得在終端機輸入的IP和端口號
    if len(sys.argv) != 3:  #一定要有3項!argv[0]:命令、argv[1]:IP、argv[2]:端口號
        print("argv is error")
        sys.exit(1)
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST,PORT)
    BUFFERSIZE = 1024
    #創建網絡連接
    sockfd = socket()
    sockfd.connect(ADDR)
    #生產事件對象
    ftp = FtpClient(sockfd) 

    while True:
        print("========命令選項=========")
        print("       (1)list          ")
        print("       (2)get file       ")
        print("       (3)put file       ")
        print("       (4)quit           ")
        print("=========================")
        data = input("輸入命令>>")
        
        #data[:?],?為取多少字
        if data[:4] == 'list':
            ftp.do_list()
            
        elif data[:3] == 'get':
            filename = data.split(' ')[-1]
            ftp.do_get(filename)
            
        elif data[:3] == 'put':
            filename = data.split(' ')[-1]#以空格分哥
            ftp.do_put(filename) 
            
        elif data[:4] == 'quit':
            ftp.do_quit()
            sockfd.close()
            sys.exit(0) 
            
        else:
            print("請輸入正確命令!")
            continue 


if __name__ == "__main__":
    main()