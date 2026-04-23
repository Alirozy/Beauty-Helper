from django.contrib import admin
from .models import CustomUser, UserProfile, UserPreferences, UserInteractions

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(UserPreferences)
admin.site.register(UserInteractions)

