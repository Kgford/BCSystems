from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.conf import settings
from atspublic import views


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    path('accounts/', include('django.contrib.auth.urls')), # new
    url(r'^$',views.index,name='public'),
    path('staff/', include("users.urls")),
    path('', include("atspublic.urls")),
    path('vendor/', include("vendor.urls")),
    #path('users/', include("users.urls")),
    path('client/', include("client.urls"),name='client'),
    path('contractors/', include("contractors.urls"),name='contractor'),
    path('inventory/', include("inventory.urls"),name='inven'),
    path('locations/', include("locations.urls")),
    path('equipment/', include("equipment.urls")),
    path('accounts/', include("accounts.urls")),
    path('dashboard/', include("dashboard.urls")),
    path('assets/', include("assets.urls")),
    path('barcodes/', include("barcode_app.urls")),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#if settings.DEBUG:
    #urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  
