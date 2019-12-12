#TCP_Ser.py

from socket import *
import time


ser = socket()

#端口號設置為立即重用
sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
ser.bind(('127.0.0.1',8888))
ser.listen(1)


print("等待接收")

con,addr = ser.accept()

print("接收到的IP位址為:",addr) # ('127.0.0.1', 42328)
print("接收到的con為:",con)
#<socket.socket fd=4, 
#family=AddressFamily.AF_INET,
#type=SocketKind.SOCK_STREAM,
#proto=0,
#laddr=('127.0.0.1', 8888),
#raddr=('127.0.0.1', 42326)>

print("等待接收中.....")
data = con.recv(1024)

#decode():是解碼
#encode()是編碼
#如果不使用data.decode()
print("1. 接收到(data):",data)
# b'\xe4\xb8\xad\xe6\x96\x87\xe7\x9a\x84\xe6\x88\x91'
print("2. 接收到(data.decode()):",data.decode())
#中文的我


print("請等我5秒鐘")
time.sleep(5)
n = con.send(b'RRRRRRRRRRRRRRR')#下方有補充知識


print("發送了:",n)
print("3秒後結束")
time.sleep(3)

con.close()
ser.close()


#------------------------------------------------
#如果不使用b'RRRRR'
#會跳出錯誤訊息:
#TypeError: a bytes-like object is required, not 'str' 
#這是說明不能是一個字符串，所以我們要把字符串轉成bytes類型
#socket網路編程中，網路傳輸都是以二進制傳輸
#在 Python3 中，當所有數據要從A台電腦傳到B台電腦時，都是以二進制傳輸，因此務必要把字符串轉成二進制

#SO_REUSEADDR
#當socket關閉後，本地端用於該socket的埠號立刻就可以被重用。通常來說，只有經過系統定義一段時間後，才能被重用。
