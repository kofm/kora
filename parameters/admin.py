""" parameter app
parameter app models managed with admin
"""
from django.contrib import admin

from .models import SpeciesParameter, Parameter, VarietalParameter

admin.site.register(Parameter)
admin.site.register(SpeciesParameter)
admin.site.register(VarietalParameter)
