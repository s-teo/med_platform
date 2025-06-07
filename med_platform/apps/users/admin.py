from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'is_staff', 'is_phone_verified', 'id')
    search_fields = ('username',)
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('is_phone_verified', 'phone', 'is_doctor')}),
    )
