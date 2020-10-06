from django.contrib import admin
from .models import Service_ChargeCodes, Service_ClassCodes, Service_CompanyInfo, Service_Customers, Service_Expenses, Service_Images, Service_Inventory, Service_Invoice, Service_InvoiceID, Service_Service, Service_Quote, Service_QuoteID, Service_Vendors, Service_ZipCode

admin.site.register(Service_ChargeCodes)
admin.site.register(Service_ClassCodes)
admin.site.register(Service_CompanyInfo)
admin.site.register(Service_Customers)
admin.site.register(Service_Expenses)
admin.site.register(Service_Images)
admin.site.register(Service_Inventory)
admin.site.register(Service_Invoice)
admin.site.register(Service_InvoiceID)
admin.site.register(Service_Service)
admin.site.register(Service_Quote)
admin.site.register(Service_QuoteID)
admin.site.register(Service_Vendors)
admin.site.register(Service_ZipCode)