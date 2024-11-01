from django.db import models


def get_model_verbose_name_plural_capitalized(model: models.Model):
    return model._meta.verbose_name_plural.capitalize()
