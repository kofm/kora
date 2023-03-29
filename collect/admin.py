from django.contrib import admin

from collect.models import Cart, CartItem, Storage, StoragePosition

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Storage)
admin.site.register(StoragePosition)
