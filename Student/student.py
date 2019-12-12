import time
import pymysql


#q)結束用的時鐘
def quit_colock():
   '''用於程式結束時紀錄的時間'''
   quit_time = time.localtime()
   t_hms = quit_time[3:6] 
   print("程序離開時間: %02d:%02d:%02d" %t_hms)


#1)增加學生資料
def add_student():
    add_data = []#新增學生資料用
    try:
        while True:
            name = input("請輸入學生名字")
            if name == ' ':
                break
            if len(name) > 20:
                while True:
                    print("學生名字超出長度20,請重新輸入")
                    name = input("請重新學生名字")
                    if len(name) <= 20:
                        break
            age = int(input("請輸入學生年齡"))
            score = int(input("請輸入學生成績"))
            d ={} #字典,有'name','age','score'
            d['name'] = name
            d['age'] = age
            d['score'] = score
            add_data.append(d) #新增一筆資料就存進列表
        showData(add_data) #顯示所有已經新增的資料
        print("您輸入的資料有:",len(add_data),"筆")
        return add_data
    except ValueError:
        print("輸入不合法")

#1)新增時顯示
#2)查看所有學生資料
def showData(stuendData):
    print('+--------------+-------+--------+')
    print('|   學生姓名   |  年齡 |  成績  |')
    print('+--------------+-------|--------+')
    try:
        for d in stuendData:
            print("|"+d['name'].ljust(14)+"|"+
            str(d['age']).ljust(7)+"|"+
            str(d['score']).ljust(8)+"|")
            print('+--------------+-------|--------+')
    except TypeError:
        print("對類型無效的操作")



#3)修改學生資料
def re_data(StData):
    name = input("請輸入要修改的學生姓名")
    fix = 0
    for st in StData:
        fix = 0
        if st['name'] == name:
            L =[]
            new_score = int(input("輸入新的成績"))
            st['score'] = new_score
            print(name ,"新成績為:",new_score)
            fix = 1
            L.append(st)
            return
    if fix == 0:
        print('查不到學生:',name)
        
        
#4)刪除學生資料
def delete_data(StData):
    name = input("請輸入要修改的學生姓名")
    #需刪除陣列中的位置
    for st in range(len(StData)):
        if StData[st]['name'] == name:
            del StData[st]
            print(name ,"已刪除")
            return
    else:
        print('查不到學生:',name)
        

#5)成績,年齡排序,顯示
#5-1)成績大到小
def Order_Score_Desc(st):
    L = sorted(st,key = lambda d:d['score'],reverse=True)
    print("成績大到小")
    showData(L)
#5-2)-成績小到大
def Order_Score_Asc(st):
    L = sorted(st,key = lambda d:d['score'])
    print("成績小到大")
    showData(L)
#5-3)-年紀大到小
def Order_Age_Desc(st):
    L = sorted(st,key = lambda d:d['age'],reverse=True)
    print("年紀大到小")
    showData(L)
#5-4)-年紀小到大
def Order_Age_Asc(st):
    L = sorted(st,key = lambda d:d['age'])
    print("年紀小到大")
    showData(L)  
    
        
#6-1)寫入txt內    
def Ser_txt(StData,filename='si.txt'):
   try:
      f = open(filename,'w')
      for stu in StData:
         #將資料轉為元組存進txt,轉為str
         da = stu['name']+','+str(stu['age'])+','+str(stu['score'])
         #print(da)
         f.write(da)
         f.write('\n')
      print("TXT檔案儲存成功!!")
      f.close()
   except OSError:
      print("保存失敗")


#6)保存文件至MySQL資料庫      
def Server_MySQL(StData):
    
    db = pymysql.connect("localhost","root","MySQL密碼",charset="utf8") #打開數據庫連接
    #print("use MySQL....") #確認是否進入DB
    #創建一個游標對象
    cur = db.cursor()
    
    cur.execute("drop database StudentDB;") #刪除名為StudentDB的資料庫
    cur.execute ("create database if not exists StudentDB;") #創建資料庫StudentDB
    cur.execute("use StudentDB;") #切換資料庫
    #創建表st1
    cur.execute("create table if not exists st1(id int ,name nvarchar(20),score int);")

    count =1     
    for i in StData:
        Myda = "insert into st1 values("+str(count)+",'"+i['name']+"',"+str(i['score'])+");"   
        cur.execute(Myda)
        count +=1 
    print("SQL資料匯入成功!!")
    #print("insert Data OK!")
    
    db.commit() #提交到數據庫
    cur.close() #關閉游標
    db.close()  #關閉數據樹連接

#7)讀取文件資料
def read_from_file(filename='si.txt'):
    L = []
    try:
        f = open(filename)
        for i in f:
            s = i.rstrip() #去掉讀進來的右側'\n'
            #print(s)
            lst = s.split(',')  #將','去掉後為['姓名','年齡','成績']
            #print(lst)
            name , age, score = lst
            age = int(age) #從str轉int
            score = int(score) #str轉int
            d ={} #字典,有'name','age','score'
            d['name'] = name
            d['age'] = age
            d['score'] = score
            L.append(d)
        print("文件讀取成功!")
        f.close()
    except OSError:
        print("文件讀取失敗")
    return L 
