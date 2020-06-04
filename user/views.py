from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.core.mail import send_mail
from utils.mixin import LoginRequiredMixin
from celery_tasks.tasks import send_active_email
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.conf import settings
from utils.code import *
from .models import *


# Create your views here.


class Checkname(View):
    def get(self, request):
        flag = False
        uname = request.GET.get('uname', "")
        # 查询用户名
        userList = UserProfile.objects.filter(username=uname)
        if userList:
            flag = True
        return JsonResponse({'flag': flag})


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        # 获取登陆表单
        if "login" in request.POST:
            user_name = request.POST.get("username", "")
            user_password = request.POST.get("pwd", "")
            user = authenticate(username=user_name, password=user_password)
            if user:
                if user.is_active:
                    next_url = request.GET.get("next", '/school/')
                    login(request, user)
                    # 确认用户信息后，将该用户存储在session中
                    # request.session['user'] = user
                    return HttpResponseRedirect(next_url)
            return HttpResponseRedirect('/login/')
        # 获取注册表单
        else:
            user_name = request.POST.get("user_name", "")
            user_password = request.POST.get("user_password", "")
            user_email = request.POST.get("user_email", "")
            user_sex = request.POST.get("user_sex", "")
            user_birth = request.POST.get("user_birth", "")
            user_phone = request.POST.get("user_phone", "")
            user = UserProfile.objects.create_user(username=user_name, password=user_password, email=user_email,
                                                   sex=user_sex, birthday=user_birth, phone=user_phone)

            # 发送激活邮件，激活连接https://127.0.0.1:8000/active/3
            serializer = Serializer(settings.SECRET_KEY, 7200)
            info = {'confirm': user.id}
            token = serializer.dumps(info).decode('utf8')

            # subject = '高校信息查询网'
            # message = ''
            # html_message = '<h1>{},欢迎注册高校信息查询网，<br>请点击您的激活连接<a href="http://127.0.0.1:8000/active/{}"></a>http://127.0.0.1:8000/active/{}</h1>'.format(
            #     user.username, token, token)
            # sender = settings.EMAIL_FROM
            # receiver = [user.email]
            # # 同步发送邮件（会导致阻塞）
            # send_mail(subject, message, sender, receiver, html_message=html_message)
            # 使用celery异步发送邮件（目前暂不支持python3.7）
            html_message = '<h1>Dear, {} !,欢迎注册高校信息查询网，<br>请点击您的激活连接<a href="http://192.168.1.247:8080/active/{}"></a>http://192.168.1.247:8080/active/{}</h1>'.format(
                user.username, token, token)
            send_active_email.delay(user.username, user.email, token, html_message)

            if user:
                # 将用户信息存放在session对象中
                # request.session['user'] = user
                return HttpResponseRedirect('/login/')


# 个人中心处理函数
class CenterView(LoginRequiredMixin, View):
    def get(self, request):
        # 获取个人信息需要先判断用户是否登陆
        # 判断函数request.user.is_authenticated()
        # 若用户为登陆request.user返回AnonymousUser类的实例
        # 模版文件可以直接获取user相关信息
        return render(request, 'center.html', {"index": True})


# 登出用户
class LogoutView(View):
    def post(self, request):
        # 删除登陆信息
        logout(request)
        # if 'user' in request.session:
        #     del request.session['user']
        return JsonResponse({'delflag': True})


# 加载验证码
class LoadCodeView(View):
    def get(self, request):
        img, str = gene_code()
        # 将生成的验证码存放到session中
        request.session['sessioncode'] = str
        return HttpResponse(img, content_type='image/png')


# 处理验证码
class CheckCodeView(View):
    def get(self, request):
        # 获取输入框中的验证码
        code = request.GET.get("code", "")
        # 获取生成的验证码
        sessioncode = request.session.get('sessioncode', None)

        flag = code.lower() == sessioncode.lower()
        return JsonResponse({'checkFlag': flag})


# 处理激活邮件
class ActiveView(View):
    def get(self, request, token):
        # 解密，获取用户信息
        serializer = Serializer(settings.SECRET_KEY, 7200)
        try:
            info = serializer.loads(token)
            user_id = info.get("confirm")
            user = UserProfile.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            return HttpResponseRedirect('/login/')
        except SignatureExpired:
            return HttpResponse('该激活链接已过期！！！')

class ReceiveEmail(View):
    def get(self, request):
        return render(request, 'ReceiveEmail.html')

    def post(self, request):
        username = request.POST.get('user_name', '')
        email = request.POST.get('email', '')
        serializer = Serializer(settings.SECRET_KEY, 7200)
        info = {'confirm': username}
        token = serializer.dumps(info).decode('utf8')
        html_message = '<h1>Dear, {} !,我们听说您丢失了高校信息查询网的密码。对于那个很抱歉！<br>但是不用担心！您可以使用下面的链接重置您的密码：<a href="http://192.168.1.247:8080/changepassword/{}"></a>http://192.168.1.247:8080/changepassword/{}</h1>'.format(
            username, token, token)
        send_active_email.delay(username, email, token, html_message)
        return HttpResponseRedirect('/login/')


class ChangePassword(View):
    def get(self, request, token):
        return render(request, 'changepassword.html')

    def post(self, request, token):
        # 解密，获取用户信息
        serializer = Serializer(settings.SECRET_KEY, 7200)
        password = request.POST.get('password', '')
        try:
            info = serializer.loads(token)
            username = info.get("confirm")
            user = UserProfile.objects.get(username=username)
            user.password = make_password(password)
            user.save()
            # update_session_auth_hash(request, username)
            return HttpResponseRedirect('/login/')
        except SignatureExpired:
            return HttpResponse('该激活链接已过期！！！')


class VerifyPassword(View):
    def get(self, request):
        flag = False
        username = request.GET.get('username', '')
        password = request.GET.get('password', '')
        print(username,password)
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                flag = True
        return JsonResponse({'checkFlag': flag})