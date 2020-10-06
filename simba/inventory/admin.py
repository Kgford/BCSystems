from django.contrib import admin
from .models import Inventory, Shelf, Events, Model, Location, Materials

# Register your models here.
admin.site.register(Inventory)
admin.site.register(Shelf)
admin.site.register(Events)
admin.site.register(Model)
admin.site.register(Location)
admin.site.register(Materials)
