from menu import *
from student import *

def main():
    ALL_StData =[] #�Ω��x�s�����ǥ͸��
    while True:
        show_menu()
        button = input("���涵��")
        if button == '1':
            print("(1) �K�[�ǥͰT��")
            if len(ALL_StData) == 0:#���0����
                ALL_StData = add_student()
            elif len(ALL_StData) > 0:
                ALL_StData += add_student() #�w�����,�إ߷s���
        elif button == '2':   
            print("(2) �d�ݩҦ��ǥͰT��")
            showData(ALL_StData)
            print("�ثe��Ƶ���:",len(ALL_StData))
        elif button == '3':
            print("(3) �ק�ǥͪ����")
            re_data(ALL_StData)
        elif button == '4':
            print("(4) �R���ǥͰT��")
            delete_data(ALL_StData)
        elif button == '5':
            print("(5) ���Z,�~�ֱƧ�")
            while True:
                Order_Windows()
                ord_s = input("�п��")
                if ord_s == '1':
                    Order_Score_Desc(ALL_StData)
                elif ord_s =='2':
                    Order_Score_Asc(ALL_StData)
                elif ord_s =='3':
                    Order_Age_Desc(ALL_StData)
                elif ord_s =='4':
                    Order_Age_Asc(ALL_StData)
                elif ord_s =='q':
                    break #��������ư��� �^��W�@��
        elif button == '6':   
            print("(6) �O�s�H��MySQL")
            Ser_txt(ALL_StData)
            Server_MySQL(ALL_StData)
        elif button == '7':
            print("(7) �qTXT�ɮ�Ū���ƾ�")
            #Ū�J�����
            if len(ALL_StData) == 0:
                ALL_StData = read_from_file()
            else:
                print("�ثe�����,Ū������")
                
        #���}���{��
        elif button == 'q' or 'Q' or 'exit' or 'EXIT':
            quit_colock()
            return


main()


