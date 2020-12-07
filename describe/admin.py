from django.contrib import admin
from .models import Protocol,Description,Trait,State,Expression

admin.site.register(Protocol)
admin.site.register(Description)
admin.site.register(Trait)
admin.site.register(State)
admin.site.register(Expression)
