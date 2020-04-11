from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from .models import *
# Create your views here.


class Checkname(View):
    def get(self,request):
        uname = request.GET.get('uname',"")



class LoginView(View):
    def get(self,request):
        return render(request,'login.html')

    def post(self,request):
        if "login" in request.POST:
            user_name = request.POST.get("user_name","")
            user_password = request.POST.get("user_password", "")
            print(user_name,user_password)
            return HttpResponseRedirect('/school/')
        else:
            user_name = request.POST.get("user_name", "")
            user_password = request.POST.get("user_password", "")
            print(user_name, user_password)
            return HttpResponseRedirect('/login/')

