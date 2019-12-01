from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from blogss.views import blog_list

urlpatterns = [

    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/', views.logout, name='logout'),
    path('user_info/', views.user_info, name='user_info'),
    path('change_nickname/',views.change_nickname,name='change_nickname'),
    path('bind_email/', views.bind_email, name='bind_email'),
    path('change_password/', views.change_password, name='change_password'),
    path('send_verify_code/',views.send_verify_code,name='send_verify_code'),
    path('forgot_password/',views.forgot_password,name='forgot_password')
]