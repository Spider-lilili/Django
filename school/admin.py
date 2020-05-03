from django.contrib import admin
from school.models import *

# Register your models here.

class BaseInfoAdmin(admin.ModelAdmin):
    list_display = ['school_id', 'school_name', 'create_time', 'address']
    search_fields = ['school_id', 'school_name', 'phone']
    ordering = ['school_id']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['school_id', 'nickname', 'like_num', 'point_num']
    search_fields = ['school_id', 'nickname']
    ordering = ['school_id']

class ContractAreaAdmin(admin.ModelAdmin):
    list_display = ['school_id', 'province', 'rate', 'num']
    search_fields = ['school_id', 'province']
    ordering = ['school_id']

# class JobrateAdmin(admin.ModelAdmin):
#     list_display = ['school_id', 'province', 'rate', 'num']
#     search_fields = ['school_id', 'province']
#     ordering = ['school_id']




admin.site.register(SchoolBaseInfo, BaseInfoAdmin)
admin.site.register(SchoolComment, CommentAdmin)
admin.site.register(SchoolContractArea, ContractAreaAdmin)

