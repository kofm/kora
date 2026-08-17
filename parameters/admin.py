"""parameter app
parameter app models managed with admin
"""

from django.contrib import admin

from .models import Parameter, VarietalParameter

admin.site.register(Parameter)
admin.site.register(VarietalParameter)
