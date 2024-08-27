from django.contrib import admin
from .models import User, ContactUs, Profile


class UserAdmin(admin.ModelAdmin):
    list_display = ['username','user_image','image','email','bio']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','full_name','phone']

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name','email','subject']


admin.site.register(User, UserAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(Profile, ProfileAdmin)
