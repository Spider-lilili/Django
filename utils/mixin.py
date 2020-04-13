# _*_coding:utf-8 _*_
"""
    @Time　　: 2020/4/13   17:23 
    @Author　 : Guoli
    @ File　　  : mixin.py
    @Software  : PyCharm
    @Description : 
"""
from django.contrib.auth.decorators import login_required


class LoginRequiredMixin():
    @classmethod
    def as_view(cls, **initkwargs):
        # 调用父类的as_view
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)
