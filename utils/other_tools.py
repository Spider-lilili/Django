# _*_coding:utf-8 _*_
"""
    @Time　　: 2020/4/20   16:01 
    @Author　 : Guoli
    @ File　　  : other_tools.py
    @Software  : PyCharm
    @Description : 
"""
from school.models import *
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage

def get_page(info, page=1, num=10):
    paginator = Paginator(info, num)
    try:
        schools = paginator.page(page)
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        schools = paginator.page(1)
    except InvalidPage:
        # 如果请求的页数不存在, 获取第一页
        schools = ''
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        schools = paginator.page(paginator.num_pages)
    return schools

def get_base_info(id):
    school_info = SchoolBaseInfo.objects.filter(school_id=id).first()
    base_info = SchoolRank.objects.filter(school_id=id).first()
    return school_info, base_info
