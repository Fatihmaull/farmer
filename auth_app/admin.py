from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Farmer


@admin.register(Farmer)
class FarmerAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'date_joined')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'address')}),
    )

