import django_tables2 as tables

from calculator.models import CropParameter

class CropParameterTable(tables.Table):
    class Meta:
      model = CropParameter
      fields = ['parameter__code', 'value']
