from django.contrib import admin
from .models import Customer, Bill, BillService

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'email', 'bill_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'mobile', 'email')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    def bill_count(self, obj):
        return obj.bill_set.count()
    bill_count.short_description = 'Total Bills'

class BillServiceInline(admin.TabularInline):
    model = BillService
    extra = 1
    readonly_fields = ('total_price_display',)
    
    def total_price_display(self, obj):
        if obj.pk:
            return f"₹{obj.total_price()}"
        return "₹0"
    total_price_display.short_description = 'Total Price'

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('bill_number', 'customer', 'total_amount', 'created_by', 'created_at')
    list_filter = ('created_at', 'created_by')
    search_fields = ('bill_number', 'customer__name', 'customer__mobile')
    readonly_fields = ('bill_number', 'created_at', 'subtotal', 'tax_amount', 'total_amount')
    inlines = [BillServiceInline]
    ordering = ('-created_at',)
    
    def service_count(self, obj):
        return obj.billservice_set.count()
    service_count.short_description = 'Services'

@admin.register(BillService)
class BillServiceAdmin(admin.ModelAdmin):
    list_display = ('bill', 'service', 'quantity', 'price', 'total_price_display')
    list_filter = ('service__category',)
    search_fields = ('bill__bill_number', 'service__name', 'bill__customer__name')
    readonly_fields = ('total_price_display',)
    
    def total_price_display(self, obj):
        return f"₹{obj.total_price()}"
    total_price_display.short_description = 'Total Price'