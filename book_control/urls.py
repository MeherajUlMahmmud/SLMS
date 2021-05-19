from django.urls import path
from .views import *
from .views import post_book_view

urlpatterns = [
    path('post-book/', post_book_view, name='post-book'),
    path('update-book/<str:pk>', update_book_view, name='update-book'),

    # path('books', book_list, name='book_list'),
    # path('<slug:department_slug>/', book_list, name='book_list_by_department'),
    path('pub/<str:slug>/', pub_book_detail_view, name='pub-book-detail'),
    path('stu/<str:slug>/', stu_book_detail_view, name='stu-book-detail'),

    path('ajax/load-departments/', load_departments, name='ajax_load_departments'),
    path('ajax/load-courses/', load_courses, name='ajax_load_courses'),
]
