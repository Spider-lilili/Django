# _*_coding:utf-8 _*_
"""
    @Time　　: 2020/4/12   17:46 
    @Author　 : Guoli
    @ File　　  : tasks.py
    @Software  : PyCharm
    @Description : 
"""
# from django.core.mail import send_mail
# from django.conf import settings
# from celery import Celery
# import django
# import os
# # django初始化
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bishe.settings')
# django.setup()

# app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/1')

# 使用celery发送邮件（异步）
# @app.task
# def send_active_email(username, to_email, token):
#     subject = '高校信息查询网'
#     message = ''
#     html_message = '<h1>{},欢迎注册高校信息查询网，<br>请点击您的激活连接<a href="http://127.0.0.1:8000/active/{}"></a>http://127.0.0.1:8000/active/{}</h1>'.format(
#         username, token, token)
#     sender = settings.EMAIL_FROM
#     receiver = [to_email]
#
#     # 同步发送邮件（会导致阻塞）
#     send_mail(subject, message, sender, receiver, html_message=html_message)
