from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect

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


class IndexView(View):
    def get(self, request, id=459):
        page = request.GET.get('page', 1)
        province = request.GET.get('province')
        type = request.GET.get('type')
        argschtype = request.GET.get('argschtype')
        schoolflag = request.GET.get('schoolflag')
        if province:
            school_info = SchoolRank.objects.filter(province_name=province).order_by('rank')
        else:
            school_info = SchoolRank.objects.all().order_by('rank')

        if type:
            school_info = school_info.filter(type_name__contains=type)
        else:
            school_info = school_info.all()

        if argschtype in ['普通本科', '独立院校', '专科']:
            school_info = school_info.filter(level_name__contains=argschtype)
        elif argschtype in ['公办', '民办']:
            school_info = school_info.filter(nature_name=argschtype)
        else:
            school_info = school_info.all()

        if schoolflag == '985':
            school_info = school_info.filter(f985=1)
        elif schoolflag == '211':
            school_info = school_info.filter(f211=1)
        elif schoolflag == '双一流':
            school_info = school_info.filter(dual_class_name=schoolflag)
        else:
            school_info = school_info.all()
        schools = get_page(school_info, page, 10)
        if schools:
            return render(request, 'index.html', {"schools": schools, "id": id, "index": True, "province":province,
                                                  "type":type, "argschtype":argschtype, "schoolflag":schoolflag})
        else:
            schools = get_page(school_info, page, 10)
            return render(request, 'index.html', {"schools": schools, "id": id, "index": True, "province":province,
                                                  "type":type, "argschtype":argschtype, "schoolflag":schoolflag})

class SchoolBase(View):
    def get(self, request, id=459):
        school_info = SchoolBaseInfo.objects.filter(school_id=id).first()
        base_info = SchoolRank.objects.filter(school_id=id).first()
        return render(request, 'school_base_info.html', {"school": school_info, "id": id, "base_info":base_info})


class ProfessionalView(View):
    def get(self, request, id=459):
        page = request.GET.get("page", 1)
        professional_list = SchoolSpecial.objects.filter(school_id=id).order_by('id')
        school_info = SchoolBaseInfo.objects.filter(school_id=id).first()
        base_info = SchoolRank.objects.filter(school_id=id).first()
        schools = get_page(professional_list, page, num=15)
        if schools:
            return render(request, 'professional.html', {"id": id, "professional_list": schools, "school": school_info, "base_info": base_info})
        else:
            schools = get_page(professional_list, 1, num=15)
            return render(request, 'professional.html', {"id": id, "professional_list": schools, "school": school_info, "base_info": base_info})


class ProvincelineView(View):
    def get(self, request, id=459):
        school_info = SchoolBaseInfo.objects.filter(school_id=id).first()
        base_info = SchoolRank.objects.filter(school_id=id).first()
        provinceline_list = SchoolProvinceline.objects.filter(school_id=id).order_by('id')
        other_provinceline = SchoolLowestScore.objects.filter(school_id=id).order_by('id')
        return render(request, 'provinceline.html', {"id": id, "provinceline_list": provinceline_list, "other_provinceline":other_provinceline, "school": school_info, "base_info": base_info})


class Job_area(View):
    def get(self, request, id=459):
        school_info = SchoolBaseInfo.objects.filter(school_id=id).first()
        base_info = SchoolRank.objects.filter(school_id=id).first()
        return render(request, 'index.html', {"id": id, "school": school_info, "base_info": base_info})


class Job_company(View):
    def get(self, request, id=459):
        school_info = SchoolBaseInfo.objects.filter(school_id=id).first()
        base_info = SchoolRank.objects.filter(school_id=id).first()
        return render(request, 'index.html', {"id": id, "school": school_info, "base_info": base_info})


class CommentView(View):
    def get(self, request, id=459):
        page = request.GET.get('page', 1)
        comment_list = SchoolComment.objects.filter(school_id=id).order_by('id')
        school_info = SchoolBaseInfo.objects.filter(school_id=id).first()
        base_info = SchoolRank.objects.filter(school_id=id).first()
        schools = get_page(comment_list, page, num=10)
        if schools:
            return render(request, 'school_comment.html', {"id": id, "comment_list": schools, "school": school_info, "base_info": base_info})
        else:
            schools = get_page(comment_list, 1, num=10)
            return render(request, 'school_comment.html', {"id": id, "comment_list": schools, "school": school_info, "base_info": base_info})




class SearchView(View):
    def post(self, request):
        school_name = request.POST.get('search','')
        print(school_name)
        if school_name:
            try:
                base_info = SchoolRank.objects.filter(school_name=school_name).first()
                school_info = SchoolBaseInfo.objects.filter(school_id=base_info.school_id).first()
                return HttpResponseRedirect('/school/{}/'.format(base_info.school_id), {"school": school_info, "base_info": base_info})
            except AttributeError:
                pass
            # return render(request, 'school_base_info.html', {"school": school_info, "base_info": base_info})

class CheckSchoolname(View):
    def get(self, request):
        flag = False
        school_name = request.GET.get('schoolname', "")
        # 查询用户名
        school_List = SchoolRank.objects.filter(school_name=school_name)
        if school_List:
            flag = True
        return JsonResponse({'flag': flag})