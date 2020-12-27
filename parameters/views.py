from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .models import Parameter

class ParametersList(ListView):
    model = Parameter

class ParametersCreate(CreateView):
    model = Parameter
    success_url = '/'
    fields = '__all__'
