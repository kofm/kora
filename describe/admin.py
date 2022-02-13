from django.contrib import admin

from .models import Description, Expression, Protocol, State, Trait

admin.site.register(Protocol)
admin.site.register(Description)
admin.site.register(Trait)
admin.site.register(State)
admin.site.register(Expression)
