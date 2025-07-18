# shop/admin.py
from datetime import timedelta
from django.contrib import admin
from .models import Category, Product, SpecialOffer

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

    def is_new(self, obj):
        return obj.created >= timezone.now() - timedelta(days=30)
    is_new.boolean = True
    is_new.short_description = 'Новинка'
    

@admin.register(SpecialOffer)
class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ('product', 'discount_percent', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('product__name',)
    date_hierarchy = 'start_date'  
    ordering = ('-start_date',)  
    
    fieldsets = (
        (None, {
            'fields': ('product', 'discount_percent')
        }),
        ('Даты акции', {
            'fields': ('start_date', 'end_date'),
            'classes': ('collapse',)
        }),
    )