from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

# Create your views here.
from .models import *
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

class LoginView(View):
    def get(self,request):
        return render(request,'login.html')


class IndexView(View):
    def get(self, request, id=459):
        page = request.GET.get('page', 1)
        school_info = SchoolRank.objects.all().order_by('id')
        schools = get_page(school_info, page, 10)
        if schools:
            return render(request, 'index.html', {"schools": schools, "id": id})
        else:
            schools = get_page(school_info, page, 10)
            return render(request, 'index.html', {"schools": schools, "id": id})


class SchoolBase(View):
    def get(self, request, id=459):
        school_info = SchoolBaseInfo.objects.filter(school_id=id).first()
        return render(request, 'school_base_info.html', {"school": school_info, "id": id})


class ProfessionalView(View):
    def get(self, request, id=459):
        page = request.GET.get("page", 1)
        professional_list = SchoolSpecial.objects.filter(school_id=id).order_by('id')
        schools = get_page(professional_list, page, num=15)
        if schools:
            return render(request, 'professional.html', {"id": id, "professional_list": schools})
        else:
            schools = get_page(professional_list, 1, num=15)
            return render(request, 'professional.html', {"id": id, "professional_list": schools})


class ProvincelineView(View):
    def get(self, request, id=459):
        provinceline_list = SchoolProvinceline.objects.filter(school_id=id).order_by('id')
        other_provinceline = SchoolLowestScore.objects.filter(school_id=id).order_by('id')
        return render(request, 'provinceline.html', {"id": id, "provinceline_list": provinceline_list,"other_provinceline":other_provinceline})


class Job_area(View):
    def get(self, request, id=459):
        return render(request, 'index.html', {"id": id})


class Job_company(View):
    def get(self, request, id=459):
        return render(request, 'index.html', {"id": id})


class CommentView(View):
    def get(self, request, id=459):
        page = request.GET.get('page', 1)
        comment_list = SchoolComment.objects.filter(school_id=id).order_by('id')
        schools = get_page(comment_list, page, num=10)
        if schools:
            return render(request, 'school_comment.html', {"id": id, "comment_list": schools})
        else:
            schools = get_page(comment_list, 1, num=10)
            return render(request, 'school_comment.html', {"id": id, "comment_list": schools})
