from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
# from celery_tasks.tasks import send_active_email
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.conf import settings
from utils.code import *
from .models import *
# Create your views here.


class Checkname(View):
    def get(self,request):
        flag = False
        uname = request.GET.get('uname',"")
        #查询用户名
        userList = UserProfile.objects.filter(username=uname)
        if userList:
            flag = True
        return JsonResponse({'flag':flag})



class LoginView(View):
    def get(self,request):
        return render(request,'login.html')

    def post(self,request):
        # 获取登陆表单
        if "login" in request.POST:
            user_name = request.POST.get("user_name", "")
            user_password = request.POST.get("pwd", "")
            print(user_password)
            user = authenticate(username=user_name, password=user_password)
            # user = UserProfile.objects.filter(username=user_name,password=user_password).first()
            if user:
                if user.is_active:
                    login(request, user)
                    # 确认用户信息后，将该用户存储在session中
                    # request.session['user'] = user
                    return HttpResponseRedirect('/school/')
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
            serializer = Serializer(settings.SECRET_KEY,7200)
            info = {'confirm': user.id}
            token = serializer.dumps(info).decode('utf8')

            subject = '高校信息查询网'
            message = ''
            html_message = '<h1>{},欢迎注册高校信息查询网，<br>请点击您的激活连接<a href="http://127.0.0.1:8000/active/{}"></a>http://127.0.0.1:8000/active/{}</h1>'.format(user.username, token, token)
            sender = settings.EMAIL_FROM
            receiver = [user.email]
            # 同步发送邮件（会导致阻塞）
            send_mail(subject, message, sender, receiver, html_message=html_message)
            # 使用celery异步发送邮件（目前暂不支持python3.7）
            # send_active_email.delay(user.username, user.email, token)


            if user:
                # 将用户信息存放在session对象中
                request.session['user'] = user
                return HttpResponseRedirect('/school/')


# 个人中心处理函数
class CenterView(View):
    def get(self,request):
        return render(request, 'center.html')

# 登出用户
class LogoutView(View):
    def post(self,request):
        # 删除登陆信息
        if 'user' in request.session:
            del request.session['user']
        return JsonResponse({'delflag':True})

# 加载验证码
class LoadCodeView(View):
    def get(self,request):
        img, str = gene_code()
        # 将生成的验证码存放到session中
        request.session['sessioncode'] = str
        return HttpResponse(img, content_type='image/png')

# 处理验证码
class CheckCodeView(View):
    def get(self,request):
        # 获取输入框中的验证码
        code = request.GET.get("code","")
        # 获取生成的验证码
        sessioncode = request.session.get('sessioncode',None)

        flag = code.lower() == sessioncode.lower()
        return JsonResponse({'checkFlag':flag})

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
            return HttpResponseRedirect('/school/')
        except SignatureExpired:
            return HttpResponse('该激活链接已过期！！！')
