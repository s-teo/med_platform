from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'username', 'is_staff', 'is_email_verified', 'id')
    search_fields = ('email', 'username')
    readonly_fields = ('phone',)
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('is_email_verified', 'phone', 'is_doctor')}),
    )
