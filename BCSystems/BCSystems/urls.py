from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.conf import settings
from test_executive import views
from django.views.static import serve

urlpatterns = [
    url(r'^users/',include('users.urls')),
    url(r'^$',views.index,name='index'),
    path("test_executive/", include("test_executive.urls")),
    path("admin/", admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
