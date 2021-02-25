from django.contrib import admin

from .models import User, Listing, Category

# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title" , "description" , "image", "category", "name", "price", "closeChecker", "date")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title" )

admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Category, CategoryAdmin)