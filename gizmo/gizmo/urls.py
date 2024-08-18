"""gizmo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.conf import settings
from users import views

urlpatterns = [
	path('admin/', admin.site.urls),
	url(r'^$',views.index,name='index'),
	url(r'^special/',views.special,name='special'),
	url(r'^users/',include('users.urls')),
	url(r'^logout/$', views.user_logout, name='logout'),
	path('gizm0/', include("gizm0.urls"),name='main'),
	path('gizm0/calibrate/', include("gizm0.urls"),name='positions'),
	path('gizm0/update/', include("gizm0.urls"),name='update'),
	path('gizm0/tray/', include("gizm0.urls"),name='tray'),
	path('ate/', include("ate.urls"),name='ate_page'),
]
