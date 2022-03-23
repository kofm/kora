from calculator.models import Crop
import math


class CropModel():
    inputs_crop = []
    context_name = 'unnamed_model'
    model_name = 'Unnamed Model'
    measure_unit = ''
    def __init__(self, crop: Crop):
        self.object = crop
        self.parameters = self.object.cropparameter_set.all()
        self.area = self.object.area

    def can_run(self):
        available_params_crop = [p.parameter.code for p in self.parameters]
        return all(x in available_params_crop for x in self.inputs_crop)

    def has_area(self):
        return self.area.total_area > 0

    def get_parameter(self, code):
        return self.parameters.get(parameter__code = code).value

    def output(self):
        context = {}
        context['model_name'] = self.model_name
        context['measure_unit'] = self.measure_unit
        return context

class CropModelExpectedYield(CropModel):
    inputs_crop = ['yield', ]
    context_name = 'expected_yield'
    model_name = 'Expected yield'
    measure_unit = 'kg'

    def can_run(self):
        return super().can_run() & self.has_area()

    def output(self):
        context = super().output()
        result = self.get_parameter('yield') * self.area.total_area
        context['value'] = result
        return context

class CropModelTotalPlants(CropModel):
    inputs_crop = ['distw', 'distb', ]
    context_name = 'total_plants'
    model_name = 'Total plants'

    def can_run(self):
        return super().can_run() & self.has_area()

    def output(self):
        context = super().output()
        nrow = math.floor(self.object.area.width / self.get_parameter('distb'))
        ncol = math.floor(1 / self.get_parameter('distw'))
        result = round(ncol * nrow * self.area.total_area,0)
        context['value'] = result
        return context
