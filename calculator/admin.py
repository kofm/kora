from django.contrib import admin

from calculator.models import Crop, CropLayout, FieldBook, Management, ManagementType

admin.site.register(CropLayout)
admin.site.register(Crop)
admin.site.register(ManagementType)
admin.site.register(Management)
admin.site.register(FieldBook)
