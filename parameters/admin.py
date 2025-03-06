"""parameter app
parameter app models managed with admin
"""

from django.contrib import admin

from .models import Parameter, SpeciesParameter, VarietalParameter

admin.site.register(Parameter)
admin.site.register(SpeciesParameter)
admin.site.register(VarietalParameter)
