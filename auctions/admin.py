from django.contrib import admin

from .models import User, Listing, Category, Bids

# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title" , "description" , "image", "category", "name", "price", "closeChecker", "date")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title" )

class BidsAdmin(admin.ModelAdmin):
    list_display = ("id", "listingId", "amount", "bidder" )

admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Bids, BidsAdmin)