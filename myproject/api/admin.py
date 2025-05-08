from django.contrib import admin
from .models import User, Order,OrderItem

# Register your models here.

class OrdeItemInline(admin.TabularInline):
    model=OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines=[
        OrdeItemInline
    ]    

admin.site.register(User)
admin.site.register(Order,OrderAdmin)
