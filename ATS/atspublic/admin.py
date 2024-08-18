from django.contrib import admin
from atspublic.models import Blog, Category, Visitor
 
class BlogAdmin(admin.ModelAdmin):
   exclude = ['posted']
   prepopulated_fields = {'slug': ('title',)}
 
class CategoryAdmin(admin.ModelAdmin):
   prepopulated_fields = {'slug': ('title',)}
 
admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Visitor)
