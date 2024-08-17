from django.contrib import admin
from .models import Specifications,TestData,TabularData,TraceData,Workstation,TestStatus,TestLogs,JobData,SpecAttachments,SpecDrawings

# Register your models here.
admin.site.register(Specifications)
admin.site.register(TestData)
admin.site.register(TabularData)
admin.site.register(TraceData)
admin.site.register(Workstation)
admin.site.register(TestStatus)
admin.site.register(TestLogs)
admin.site.register(JobData)
admin.site.register(SpecAttachments)
admin.site.register(SpecDrawings)
