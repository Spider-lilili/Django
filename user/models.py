# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    """
    自定义用户表单
    """
    username = models.CharField(max_length=20, verbose_name='昵称', default='', unique=True)
    password = models.CharField(max_length=100, verbose_name='密码')
    email = models.EmailField(max_length=50, verbose_name='邮件')
    sex = models.CharField(max_length=50, verbose_name='性别')
    birthday = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=11, verbose_name='手机')
    last_login = models.DateTimeField(blank=True, null=True, )
    is_superuser = models.IntegerField(default=0)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    is_staff = models.IntegerField()
    is_active = models.IntegerField(default=0)

    def __str__(self):
        return self.username


# class UserInfo(models.Model):
#     nickname = models.CharField(max_length=100, unique=True)
#     password = models.CharField(max_length=100)
#     email = models.EmailField(max_length=50)
#     sex = models.CharField(max_length=50)
#     birthday = models.DateField()
#     phone = models.CharField(max_length=11)
#
#     def __str__(self):
#         return self.nickname
#
#
# class UserBaseInfo(models.Model):
#     real_name = models.CharField(max_length=50)
#     identity_number = models.CharField(max_length=18)
#     age = models.CharField(max_length=10)
#     address = models.CharField(max_length=100)
#     description = models.CharField(max_length=500)
#     userinfo = models.ForeignKey(UserInfo,on_delete=models.CASCADE)
#
#     def __str__(self):
#         return "{}, {}".format(self.userinfo.nickname,self.real_name)
