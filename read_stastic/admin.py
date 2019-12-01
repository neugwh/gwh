from django.contrib import admin

# Register your models here.
from read_stastic.models import ReadNum, ReadDetail


@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_num','content_object')
@admin.register(ReadDetail)
class ReadDeatilAdmin(admin.ModelAdmin):
    list_display = ('date','read_num','content_object')