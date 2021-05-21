from django.contrib import admin
from .models import *


# class StudentProfileModelAdmin(admin.ModelAdmin):
#     list_display = ('university', 'department')
#     search_fields = ('university',)
#     readonly_fields = ()
#
#     filter_horizontal = ()
#     ordering = ()
#     fieldsets = ()
#     list_filter = ()
#
#
# class PublisherProfileModelAdmin(admin.ModelAdmin):
#     list_display = ('university', 'department')
#     search_fields = ('university',)
#     readonly_fields = ()
#
#     filter_horizontal = ()
#     ordering = ()
#     fieldsets = ()
#     list_filter = ()


admin.site.register(User)
admin.site.register(StudentProfileModel)
admin.site.register(PublisherProfileModel)
