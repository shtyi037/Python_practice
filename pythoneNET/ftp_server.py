#ftp_server.py
from socket import *
import os 
import sys
import signal 
import time

FILE_PATH = "/home/tarena/"

class FtpServer(object):
    def __init__(self,connfd):
        self.connfd = connfd

    def do_list(self):
        #指定FILE_PATH路徑的文件
        filelist = os.listdir(FILE_PATH)
        
        #服務器確認請求是否可以執行
        if filelist == None:
            #如果不存在此文件,回傳FALL
            self.connfd.send(b"FALL") 
        self.connfd.send(b'OK')#確認有文件後,回傳OK給客戶端
        time.sleep(0.1)#如不使用sleep可能會出現沾包
        for filename in filelist:
            #文件不是'.'開頭(隱藏文件) 且 是普通文件 (isfile回傳Ture)
            #不能只有文件名,isfile要有(正確的路徑名)
            if filename[0] != '.' and os.path.isfile(FILE_PATH + filename):
                self.connfd.send(filename.encode())#回傳文件名稱給客戶端
                time.sleep(0.1)
        #告知客戶端,##為 發送完        
        self.connfd.send(b"##")
        print("文件列表發送完畢")
        return
    
    #server發送給client客戶端
    def do_get(self,filename):
        try:
            #在server端先確認是否有該文件
            fd = open(FILE_PATH+filename,'rb')
        except:
            #文件不存在,傳失敗訊息給客戶端
            self.connfd.send(b"FALL") 
        self.connfd.send(b'OK')#確認有該文件則回傳給客戶端OK
        time.sleep(0.1)
        #開始發送文件中的內容
        for line in fd:
            self.connfd.send(line)
        fd.close()
        time.sleep(0.1)
        #最後發送結束的提示給客戶端
        self.connfd.send(b'##')
        
        print("文件發送成功")
        return

    def do_put(self,filename):
        try:
            fd = open(FILE_PATH+filename,'w')
        except:
            self.connfd.send(b"FALL") 
        self.connfd.send(b'OK')
        while True:
            data = self.connfd.recv(1024).decode()
            if data == '##':
                break
            fd.write(data)
        fd.close()
        print("接收文件完畢")
        return

def main():
    #取得在終端機輸入的IP和端口號
    if len(sys.argv) != 3: #一定要有3項!argv[0]:命令、argv[1]:IP、argv[2]:端口號
        print("argv is error")
        sys.exit(1)
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST,PORT)
    BUFFERSIZE = 1024
    #創建網絡連接
    sockfd = socket()
    sockfd.bind(ADDR)
    sockfd.listen(5)
    #處理殭屍進程
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    while True:
        #確保能夠連接正常
        try:
            connfd,addr = sockfd.accept()
        #用戶中斷執行 Ctrl+C
        except KeyboardInterrupt: 
            sockfd.close()
            sys.exit(0)
        except Exception:
            continue
        print("客戶端登入:",addr)
        
        #創建子進程
        pid = os.fork()
        if pid < 0:
            print("創建子進程失敗")
            continue
        #子進程
        elif pid == 0:
            sockfd.close()
            ftp = FtpServer(connfd)
            #接收Client(客?端)的請求
            while True:
                #子進程的第一次接收
                data = connfd.recv(BUFFERSIZE).decode()
                #判斷client(客戶端)傳過來的第一個字母
                if data[0] == 'L':
                    ftp.do_list() 
                
                elif data[0] == 'G':#Get 客戶端要下載文件
                    filename = data.split(' ')[-1]
                    ftp.do_get(filename)
                elif data[0] == "P":
                    filename = data.split(' ')[-1]
                    ftp.do_put(filename)
                #子進程退出
                elif data[0] == "Q":
                    print("客戶端退出")
                    sys.exit(0)
        #父進程會繼續接收
        else:
            connfd.close()
            continue


if __name__ == "__main__":
    main()
