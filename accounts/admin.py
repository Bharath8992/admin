from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Fields to display in the admin list view
    list_display = (
        'username', 'email', 'phone', 'membership_type', 
        'is_staff', 'is_active', 'date_joined'
    )
    list_filter = ('membership_type', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'email', 'phone')
    ordering = ('username',)

    # Fieldsets for viewing/editing an existing user
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'membership_type')}),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            ),
        }),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields for the user creation form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'phone', 'membership_type',
                'password1', 'password2', 'is_active', 'is_staff'
            ),
        }),
    )

    # Optional: make sure email is required when adding users
    def save_model(self, request, obj, form, change):
        if not obj.email:
            raise ValueError("Email is required for all users.")
        super().save_model(request, obj, form, change)
