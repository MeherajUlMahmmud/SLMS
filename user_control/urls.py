from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', home, name='home'),

    # user login and logout url
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('publisher-register', publisher_register_view, name='publisher-register'),
    path('student-register', student_register_view, name='student-register'),
    
    # student and publisher dashboard url
    path('student/student-dashboard', student_dashboard_view, name='student-dashboard'),
    path('publisher/publisher-dashboard', publisher_dashboard_view, name='publisher-dashboard'),

    path('profile/<str:pk>', profile_view, name='profile'),
    path('profile/edit/<str:pk>', profile_update_view, name='profile-update'),

    path('account-settings/', account_settings, name='settings'),
    path('about', about_view, name='about'),
    path('contact', contact_view, name='contact'),
]
