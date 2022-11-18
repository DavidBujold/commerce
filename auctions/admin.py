from django.contrib import admin

from auctions.models import Category, Listing, Bids, Comments

# Register your models here.
admin.site.register(Listing)
admin.site.register(Category)
admin.site.register(Bids)
admin.site.register(Comments)
