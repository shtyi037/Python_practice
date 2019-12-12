#TCP_Cli.py

from socket import *
import time


cli = socket()

cli.connect(('127.0.0.1',8888))

c_data = input("請輸入")
#decode():是解碼
#encode()是編碼
cli.sendall(c_data.encode())

#客戶端接收
s_data = cli.recv(1024)
print("Clien收到:",s_data)


print("準備斷開客戶端連接")
time.sleep(2)

cli.close()




#可參考:
#https://ithelp.ithome.com.tw/articles/10185614