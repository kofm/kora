import re

from django.db import models


def get_model_verbose_name_plural_capitalized(model: models.Model):
    return model._meta.verbose_name_plural.capitalize()


def smart_truncate_string(text, min_length=10, suffix="..."):
    """If the `text` is more than `min_length` characters long, it
    will be cut at the next word-boundary and `suffix` will be
    appended.
    https://stackoverflow.com/a/250471/2791638
    """
    pattern = r"^(.{%d,}?\S)\s.*" % (min_length - 1)
    return re.sub(pattern, r"\1" + suffix, text)
