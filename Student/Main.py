from menu import *
from student import *

def main():
    ALL_StData =[] #用於儲存全部學生資料
    while True:
        show_menu()
        button = input("執行項目")
        if button == '1':
            print("(1) 添加學生訊息")
            if len(ALL_StData) == 0:#資料0筆時
                ALL_StData = add_student()
            elif len(ALL_StData) > 0:
                ALL_StData += add_student() #已有資料,建立新資料
        elif button == '2':   
            print("(2) 查看所有學生訊息")
            showData(ALL_StData)
            print("目前資料筆數:",len(ALL_StData))
        elif button == '3':
            print("(3) 修改學生的資料")
            re_data(ALL_StData)
        elif button == '4':
            print("(4) 刪除學生訊息")
            delete_data(ALL_StData)
        elif button == '5':
            print("(5) 成績,年齡排序")
            while True:
                Order_Windows()
                ord_s = input("請選擇")
                if ord_s == '1':
                    Order_Score_Desc(ALL_StData)
                elif ord_s =='2':
                    Order_Score_Asc(ALL_StData)
                elif ord_s =='3':
                    Order_Age_Desc(ALL_StData)
                elif ord_s =='4':
                    Order_Age_Asc(ALL_StData)
                elif ord_s =='q':
                    break #結束此函數執行 回到上一頁
        elif button == '6':   
            print("(6) 保存信息MySQL")
            Ser_txt(ALL_StData)
            Server_MySQL(ALL_StData)
        elif button == '7':
            print("(7) 從TXT檔案讀取數據")
            #讀入的資料
            if len(ALL_StData) == 0:
                ALL_StData = read_from_file()
            else:
                print("目前有資料,讀取失敗")
                
        #離開此程式
        elif button == 'q' or 'Q' or 'exit' or 'EXIT':
            quit_colock()
            return


main()


