from django.contrib import admin

from auctions.models import Category, Listing, Bids

# Register your models here.
admin.site.register(Listing)
admin.site.register(Category)
admin.site.register(Bids)
