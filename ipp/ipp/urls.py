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
    url(r'^user_login/$', views.user_login, name='login'),
    path('inventory/', include("inventory.urls")),
    path('stock/', include("stock.urls")),
    path('inspection/', include("qa.urls")),
    path('sales/', include("sales.urls")),
    path('barcodes/', include("barcode_app.urls")),
    #path('processes/', include("process.urls")),
    #path('shipping/', include("shipping.urls")),
    #path('planning/', include("planning.urls")),
    #path('manufacturing/', include("manufacturing.urls")),
   
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
