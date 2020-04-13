"""bishe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path('^login/$', views.LoginView.as_view()),
    re_path('^checkname/$', views.Checkname.as_view()),
    re_path('^center/$', views.CenterView.as_view()),
    re_path('^logout/$', views.LogoutView.as_view()),
    re_path('^loadcode/$', views.LoadCodeView.as_view()),
    re_path('^checkcode/$', views.CheckCodeView.as_view()),
    re_path('^active/(?P<token>.*)$', views.ActiveView.as_view()),
]


