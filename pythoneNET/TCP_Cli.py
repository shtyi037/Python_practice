#TCP_Cli.py

from socket import *
import time


cli = socket()

cli.connect(('127.0.0.1',8888))

c_data = input("�п�J")
#decode():�O�ѽX
#encode()�O�s�X
cli.sendall(c_data.encode())

#�Ȥ�ݱ���
s_data = cli.recv(1024)
print("Clien����:",s_data)


print("�ǳ��_�}�Ȥ�ݳs��")
time.sleep(2)

cli.close()




#�i�Ѧ�:
#https://ithelp.ithome.com.tw/articles/10185614