from django.contrib import admin
from .models import ServiceCategory, Service

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_count', 'description_preview')
    list_filter = ('name',)
    search_fields = ('name', 'description')
    ordering = ('name',)
    
    def service_count(self, obj):
        return obj.service_set.count()
    service_count.short_description = 'Services Count'
    
    def description_preview(self, obj):
        return obj.description[:50] + '...' if obj.description else '-'
    description_preview.short_description = 'Description Preview'

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'duration', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'category__name')
    list_editable = ('price', 'duration', 'is_active')
    ordering = ('category', 'name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'description')
        }),
        ('Pricing & Details', {
            'fields': ('price', 'duration', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )