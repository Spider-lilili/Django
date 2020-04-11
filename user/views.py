from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse

from utils.code import *
from .models import *
# Create your views here.


class Checkname(View):
    def get(self,request):
        flag = False
        uname = request.GET.get('uname',"")
        #查询用户名
        userList = UserInfo.objects.filter(nickname=uname)
        if userList:
            flag = True
        return JsonResponse({'flag':flag})



class LoginView(View):
    def get(self,request):
        return render(request,'login.html')

    def post(self,request):
        if "login" in request.POST:
            user_name = request.POST.get("user_name", "")
            user_password = request.POST.get("pwd", "")
            user = UserInfo.objects.filter(nickname=user_name,password=user_password).first()
            if user:
                request.session['user'] = user
                return HttpResponseRedirect('/school/')
            return HttpResponseRedirect('/login/')
        else:
            user_name = request.POST.get("user_name", "")
            user_password = request.POST.get("user_password", "")
            user_email = request.POST.get("user_email", "")
            user_sex = request.POST.get("user_sex", "")
            user_birth = request.POST.get("user_birth", "")
            user_phone = request.POST.get("user_phone", "")
            user = UserInfo.objects.create(nickname=user_name, password=user_password, email=user_email,
                                                sex=user_sex, birthday=user_birth, phone=user_phone)
            if user:
                # 将用户信息存放在session对象中
                request.session['user'] = user
                return HttpResponseRedirect('/school/')


class CenterView(View):
    def get(self,request):
        return render(request, 'center.html')


class LogoutView(View):
    def post(self,request):
        # 删除登陆信息
        if 'user' in request.session:
            del request.session['user']
        return JsonResponse({'delflag':True})


class LoadCodeView(View):
    def get(self,request):
        img, str = gene_code()
        # 将生成的验证码存放到session中
        request.session['sessioncode'] = str
        return HttpResponse(img, content_type='image/png')


class CheckCodeView(View):
    def get(self,request):
        # 获取输入框中的验证码
        code = request.GET.get("code","")
        # 获取生成的验证码
        sessioncode = request.session.get('sessioncode',None)

        flag = code == sessioncode
        return JsonResponse({'checkFlag':flag})