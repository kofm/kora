""" parameter app
parameter app models managed with admin
"""
from django.contrib import admin

from .models import CropParameter, Measure, Parameter, VarietalParameter

admin.site.register(Parameter)
admin.site.register(CropParameter)
admin.site.register(VarietalParameter)
admin.site.register(Measure)
