from django.contrib import admin
from .models import Inventory, Shelf, Events

# Register your models here.
admin.site.register(Inventory)
admin.site.register(Shelf)
admin.site.register(Events)
