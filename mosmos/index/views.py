from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *

# Create your views here.
# def login_views(request):
#     #判斷request.method 是get還是post
#     if request.method =='GET':
#         return render(request,'login.html')
#     else:
#         uphone = request.POST.get('uphone','')
#         upwd = request.POST.get('upwd','')
#         # if uphone and upwd:
#         #     users = Mos.objects.filter(uphone=uphone, upass=upwd)
#         #     if users:
#         #         return HttpResponse('登錄成功!!')
#         #     else:
#         #         errMsg ='手機號碼或密碼不正確'
#         #         return render(request,'login.html',locals())
#         if uphone and upwd:
#             users = Mos.objects.filter(uphone=uphone)
#             if users:
#                 u = users[0] #Mos objects
#                 if upwd == u.upass:
#                     return HttpResponse('登錄成功')
#                 else:
#                     errMsg = '您輸入的密碼不正確'
#                     return render(request, 'login.html', locals())
#             else:
#                 errMsg = '您輸入的手機號碼不存在'
#                 return render(request, 'login.html', locals())
#         else:
#             errMsg ='手機號碼或密碼不能為空'
#             return render(request,'login.html',locals())

def login_views(request):
    #執行登入的驗證判斷,POST or GET   
    if request.method == "POST":
        uphone = request.POST.get('uphone','')
        upwd = request.POST.get('upwd','')
        #同為驗證功能,檢查輸入的帳密與資料庫(Mos)是否正確
        uList = Mos.objects.filter(uphone=uphone, upass=upwd)
        if uList:
            #登入成功
            resp = HttpResponseRedirect('/index/')
            #將手機號碼存進session,密碼不存
            request.session['uphone'] = uphone
            #判斷是否要存進cookies
            if 'isSave' in request.POST:
                print("set SAVE")
                #儲存手機號碼,並設定365天(秒*分*時*天)
                resp.set_cookie('uphone',uphone,360*24*365)
            return resp
        else:
            #登入失敗
            errMsg = '手機號碼或密碼不正確'
            return render(request, 'login.html', locals())
    #GET時,判斷是否處於已登入的狀態(session中是否有值)
    else:
        if 'uphone' in request.session:
            return HttpResponseRedirect('/index/')
        else:
            #處於未登入狀態,即判斷曾經是否有登入過(cookies中是否有值,有的話則取值)
            if 'uphone' in request.COOKIES:
                #過去曾登入過,取出值後存入session
                uphone = request.COOKIES['uphone']
                request.session['uphone'] = uphone
                return HttpResponseRedirect('/index/')
            else:
                #沒有登入過
                return render(request, 'login.html')

def index_views(request):
    return render(request,'index.html')


def register_views(request):
    # 判斷request.method 得到用户的意圖
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        # 實現註冊操作
        uphone = request.POST.get('uphone', '')
        upwd = request.POST.get('upwd', '')
        uname = request.POST.get('uname', '')
        uemail = request.POST.get('uemail', '')

        if uphone and upwd and uname and uemail:
            #先判斷uphone的數據是否存在
            u = Mos.objects.filter(uphone=uphone)
            if u:
                errMsg = '手機號碼已存在'
                return render(request, 'register.html', locals())
            else:
                #創建資料
                Mos.objects.create(uphone=uphone, upass=upwd,uname=uname, uemail=uemail)
                return HttpResponse('註冊成功!!')
        else:
            return HttpResponse('數據不能為空')
