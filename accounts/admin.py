# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'phone', 'get_membership_type', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'date_joined')
    search_fields = ('email', 'username', 'phone')
    ordering = ('email',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('phone',)}),
    )
    
    def get_membership_type(self, obj):
        """Get membership type from related membership object"""
        if hasattr(obj, 'membership'):
            return obj.membership.membership_type
        return 'No Membership'
    get_membership_type.short_description = 'Membership Type'
    get_membership_type.admin_order_field = 'membership__membership_type'