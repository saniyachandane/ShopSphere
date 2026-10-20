from django.contrib import admin
from .models import Category,Product,Order, OrderItem

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('id','name','description')
    search_fields=('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('id','name','category','price','stock','created_at')
    list_filter=('category','created_at')
    search_fields=('name','description')
    ordering=('-created_at',)

admin.site.register(Order)
admin.site.register(OrderItem)