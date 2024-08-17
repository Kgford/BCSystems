from django.contrib import admin
from users.models import UserProfileInfo,User,PTOAccruals

# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(PTOAccruals)