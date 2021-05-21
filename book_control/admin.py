from django.contrib import admin
from .models import *


class DepartmentModelAdmin(admin.ModelAdmin):
    list_display = ('university', 'department')
    search_fields = ('university',)
    readonly_fields = ()

    filter_horizontal = ()
    ordering = ()
    fieldsets = ()
    list_filter = ()


class CourseModelAdmin(admin.ModelAdmin):
    list_display = ('university', 'department', 'course',)
    search_fields = ('university',)
    readonly_fields = ()

    filter_horizontal = ()
    ordering = ()
    fieldsets = ()
    list_filter = ()


admin.site.register(UniversityModel)
admin.site.register(DepartmentModel, DepartmentModelAdmin)
admin.site.register(CourseModel, CourseModelAdmin)
admin.site.register(BookModel)
