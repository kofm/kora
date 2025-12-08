from django.contrib import admin

from collect.models import Cart, CartItem, Sample, Storage, StoragePosition


class CartAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        if obj is not None:
            return obj.user == request.user
        return super().has_view_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            return obj.user == request.user
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            return obj.user == request.user
        return super().has_delete_permission(request, obj)


admin.site.register(Sample)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Storage)
admin.site.register(StoragePosition)
