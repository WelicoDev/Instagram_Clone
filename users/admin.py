from django.contrib import admin
from .models import User , UserConfirmation
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['id' , 'email','phone_number' , 'username']

admin.site.register(User, UserAdmin)
admin.site.register(UserConfirmation)