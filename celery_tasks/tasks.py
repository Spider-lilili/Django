# _*_coding:utf-8 _*_
"""
    @Time　　: 2020/4/12   17:46 
    @Author　 : Guoli
    @ File　　  : tasks.py
    @Software  : PyCharm
    @Description : 
"""
import time

from django.core.mail import send_mail
from django.conf import settings
from celery import Celery
import django
import os
# django初始化
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bishe.settings')
django.setup()

app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/1')

# 使用celery发送邮件（异步）
@app.task
def send_active_email(username, to_email, token, html_message):
    subject = '高校信息查询网'
    message = ''

    sender = settings.EMAIL_FROM
    receiver = [to_email]

    # 同步发送邮件（会导致阻塞）
    send_mail(subject, message, sender, receiver, html_message=html_message)
    time.sleep(5)
