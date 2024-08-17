from django.urls import path
from django.conf.urls import url,include
from django.conf.urls.static import static
from test_executive import views
from django.conf import settings
from django.contrib import admin
admin.autodiscover()
from django.contrib.auth.decorators import login_required, permission_required
from test_executive.views import (
    TestExec,
    update_offset,  
)


app_name = "test_exec"

urlpatterns =[
    path('', login_required(TestExec.as_view(template_name="test_exec.html")), name='test_exec'),
    path('update_offset/', update_offset, name = "update_offset"),    
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    
# customizing admin interface
admin.site.site_header = 'Automated Test Solutions'
admin.site.site_title = 'Automated Test Solutions'
admin.site.index_title = 'Automated Test Solutions Administration'
  
