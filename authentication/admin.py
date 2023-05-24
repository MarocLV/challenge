from django.contrib import admin
from .models import CustomUser, HitmanProfile, Roles
# Register your models here.


admin.site.register(CustomUser)
admin.site.register(HitmanProfile)
admin.site.register(Roles)