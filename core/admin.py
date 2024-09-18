from django.contrib import admin
from . import models

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ['name']
    }

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ['category', 'name']
    }
    list_display = ['name', 'category', 'price', 'count']
    search_fields = ['name']
    list_filter = ['category', 'created_at']

admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Cart)
admin.site.register(models.Review)