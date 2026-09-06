from django.contrib import admin

from collect.models import Cart, CartItem, Sample, Storage, StoragePosition


admin.site.register(Sample)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Storage)
admin.site.register(StoragePosition)
