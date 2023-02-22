from django.utils.safestring import mark_safe
import django_tables2 as tables

from calculator.models import CropParameter

class CropParameterTable(tables.Table):
    class Meta:
      model = CropParameter
      fields = ['parameter__code', 'value']

class CropStatisticsTable(tables.Table):
    common_name = tables.Column(verbose_name="Common name")
    total_area = tables.Column(verbose_name=mark_safe("Total area (m<sup>2</sup>)"))
    class Meta:
        template_name = "django_tables2/bootstrap.html"
