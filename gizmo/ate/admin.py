from django.contrib import admin
from .models import Specifications, Trace, Trace_points, Testdata, Effeciency, Workstation

# Register your models here.
admin.site.register(Specifications)
admin.site.register(Trace)
admin.site.register(Trace_points)
admin.site.register(Testdata)
admin.site.register(Effeciency)
admin.site.register(Workstation)


