#ftp_client.py
from socket import * 
import sys 
import time

class FtpClient(object):
    def __init__(self,sockfd):
        self.sockfd = sockfd

    def do_list(self):
        self.sockfd.send(b"L") #�o�e�ШD����
        #�����A�Ⱦ��T�{ OK �� FALL
        data = self.sockfd.recv(1024).decode()
        if data == 'OK':
            #���\,�`������server�^�ǹL�Ӫ����W
            while True:
                data = self.sockfd.recv(1024).decode()
                if data == '##': #����server�ݧi���������T��
                    break
                print(data)
            print("���C��i�ܧ���")
            return
        else:
            #����
            print("���C��ШD����")
            return

    def do_get(self,filename):
        self.sockfd.send(("G " + filename).encode())
        #�����A�Ⱦ��T�{ OK �� FALL
        data = self.sockfd.recv(1024).decode()
        if data == 'OK':
            fd = open(filename,'w')
            while True:
                #����server�ݵo�e����r,�g�J���
                data = self.sockfd.recv(1024).decode()
                if data == '##':
                #����##�h����
                    break
                fd.write(data)
            fd.close()
            print('%s �U������'%filename)
            return
        else:
            print("�U����󥢱�")
            return

    def do_put(self,filename):
        try:
            fd = open(filename,'rb')
        except:
            print("�W�Ǫ���󥢱�")
            return 
        self.sockfd.send(("P " + filename).encode())
        #�����A�Ⱦ��T�{ OK �� FALL
        data = self.sockfd.recv(1024).decode()
        if data == 'OK':
            for line in fd:
                self.sockfd.send(line)
            fd.close()
            time.sleep(0.1)
            self.sockfd.send(b"##")
            print("�W�Ǥ��@%s�@����"%filename)
            return 
        else:
            print("�W�Ǥ�󥢱�")
            return

    def do_quit(self):
        self.sockfd.send(b"Q")

def main():
    #���o�b�׺ݾ���J��IP�M�ݤf��
    if len(sys.argv) != 3:  #�@�w�n��3��!argv[0]:�R�O�Bargv[1]:IP�Bargv[2]:�ݤf��
        print("argv is error")
        sys.exit(1)
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST,PORT)
    BUFFERSIZE = 1024
    #�Ыغ����s��
    sockfd = socket()
    sockfd.connect(ADDR)
    #�Ͳ��ƥ��H
    ftp = FtpClient(sockfd) 

    while True:
        print("========�R�O�ﶵ=========")
        print("       (1)list          ")
        print("       (2)get file       ")
        print("       (3)put file       ")
        print("       (4)quit           ")
        print("=========================")
        data = input("��J�R�O>>")
        
        #data[:?],?�����h�֦r
        if data[:4] == 'list':
            ftp.do_list()
            
        elif data[:3] == 'get':
            filename = data.split(' ')[-1]
            ftp.do_get(filename)
            
        elif data[:3] == 'put':
            filename = data.split(' ')[-1]#�H�Ů����
            ftp.do_put(filename) 
            
        elif data[:4] == 'quit':
            ftp.do_quit()
            sockfd.close()
            sys.exit(0) 
            
        else:
            print("�п�J���T�R�O!")
            continue 


if __name__ == "__main__":
    main()