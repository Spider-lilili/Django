# _*_coding:utf-8 _*_
"""
    @Time　　: 2020/4/11   15:37 
    @Author　 : Guoli
    @ File　　  : mycontentprocessors.py
    @Software  : PyCharm
    @Description : 
"""
def getUserinfo(request):
    return {'suser':request.session.get("user",None)}


