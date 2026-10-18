"""parameter app
parameter app models managed with admin
"""

from django.contrib import admin

from .forms import ParameterForm
from .models import Parameter, VarietalParameter


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    form = ParameterForm


admin.site.register(VarietalParameter)
