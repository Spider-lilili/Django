from django.db import models

# Create your models here.


class UserInfo(models.Model):
    nickname = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    sex = models.CharField(max_length=50)
    birthday = models.DateField()
    phone = models.CharField(max_length=11)

    def __str__(self):
        return self.nickname


class UserBaseInfo(models.Model):
    real_name = models.CharField(max_length=50)
    identity_number = models.CharField(max_length=18)
    age = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    userinfo = models.ForeignKey(UserInfo,on_delete=models.CASCADE)

    def __str__(self):
        return "{}, {}".format(self.userinfo.nickname,self.real_name)