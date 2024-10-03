from django.contrib import admin
from .models import Order

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'price', 'status']
    search_fields = ['user', 'products']
    list_filter = ['created_at']

admin.site.register(Order, OrderAdmin)