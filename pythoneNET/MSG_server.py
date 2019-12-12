#MSG_server.py
from socket import *
import time,threading, select,sys 




L = []#存放客戶端名稱
#客戶端名稱
def clientName(addr,name):
    dic = {'addr':addr,'name':name}
    L.append(dic)


#廣播功能->新用戶加入
def NewUser(name):
    for n in L:
        if n['name'] is name:
            continue
        sayHello = '新用戶:'+ name
        n['addr'].send(sayHello.encode())

#廣播功能->用戶離開
def Userleaving(addr):
    global L
    leavName ='N'
    #先找尋使用者名稱
    for n in L:
        if n['addr'] is addr:
            leavName = n['name']
            L.remove(n)
    for s in L:
        sayHello = leavName+' 離開聊天室'
        s['addr'].send(sayHello.encode())
    print(leavName,"離開")
        
#對話傳給聊天室的所有人
def Msg_all(addr,data):
    global L
    leavName ='N'
    #先找尋名稱
    for n in L:
        if n['addr'] != addr:#傳給除了自己以外的使用者
            n['addr'].send(data.encode())



#發給Client的訊息
def broadSend(conn):
    #為了維持持續的發送
    while True:
        data = input(">>>")
        if data =='exit':
            xlist.append(conn)
        for n in L:
            psdata = "Server >> "+data
            n['addr'].send(psdata.encode())
            print("發給",n['name'],"訊息:",data)


def main():

    count = 0
    global L_Server,rlist,wlist,xlist
    thread_send = threading.Thread(target=broadSend, args=(L_Server, )) #發
    thread_send.setDaemon(True)#子線程隨主線​​程的結束
    thread_send.start()
    while True:
        rs, ws, es = select.select(rlist,wlist,xlist)
        for r in rs:
            #如果是新客戶端,則新增
            if r is L_Server:
                con ,addr = L_Server.accept()#接收客戶端
                print("新客戶端連線",addr)
                rlist.append(con)
                xlist.append(con)#確保後續異常會處理
            #已可接收資料
            else:
                #先接收資料,來判斷要做什麼內容
                data = r.recv(BUFFERSIZE).decode()#解密
                #如果無資料->離開
                if not data or data =='exit':
                    Userleaving(r)
                    rlist.remove(r)
                    xlist.remove(r)
                    r.close()#斷開連結
                        
                #有資料
                else:
                    #第一次接收客戶端姓名並儲存在Server
                    if data[:4]=='name':
                        name = data[5:]
                        print("收到客戶端名稱:",name)
                        clientName(r,name)
                        #發送廣播告知所有客戶有新客戶端
                        NewUser(name)
                    #收到的客戶端名稱及訊息
                    else:
                        #wlist.append(r)#收到訊息,要主動回傳給對方
                        for n in L:
                            if r is n['addr']: 
                                print(n['name'],">>>",data)
                                spdata = n['name'] + ">>>" +data
                                Msg_all(r,spdata)
                                
#--------------------------------------------------------------------        
        #需回覆給對方的訊息
        for w in ws:
            print("WWWW裡面")
            w.send("已收到訊息!".encode())
            wlist.remove(w)#回傳訊息後刪除
            print("server發送訊息完畢!")
        #發生異常通知你處理的事件
        for e in es:
            print("執行E")
            if e is L_Server:
                print("伺服器即將關閉!")
                time.sleep(5)
                L_Server.close()
                sys.exit()
            else:
                print("有人離開")
                rlist.remove(e)
                xlist.remove(e)
                #關閉客戶端
                e.close()
        print("----------------------------------:",count)
        count +=1


#一定要有3項
if len(sys.argv) !=3:
    print("argv is Error!!!!")
    sys.exit(1)
HOST = sys.argv[1]
PORT = int(sys.argv[2])
ADDR = (HOST,PORT)
BUFFERSIZE = 1024
#創建網絡連接
L_Server = socket()
L_Server.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
L_Server.bind(ADDR)#與伺服器連接
L_Server.listen(5)
rlist = [L_Server]
wlist = []
xlist = [L_Server]

main()

