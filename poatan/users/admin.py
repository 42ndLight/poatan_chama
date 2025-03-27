from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_no', 'role')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_no', 'role')

admin.site.register(User, UserAdmin)