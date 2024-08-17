from django.conf.urls import url
from django.contrib.auth import views as auth_views
from users import views
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required

from users.views import (
    ProfileView,
 
)
# SET THE NAMESPACE!
app_name = 'users'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'), 
    url(r'^password_reset/$',views.user_login,name='password_reset'), 
    url(r'^$',views.index,name='base'),
    url(r'^special/',views.special,name='special'),
    url(r'^logout/$', views.user_logout, name='logout'),    
    path('profiles/', login_required(ProfileView.as_view(template_name="user_profiles.html")), name='profiles'),
]
