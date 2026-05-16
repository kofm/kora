from django.db import models


class Label(models.Model):
    class Colour(models.TextChoices):
        GRAY = "gray", "Gray"
        BLUE = "blue", "Blue"
        INDIGO = "indigo", "Indigo"
        PURPLE = "purple", "Purple"
        PINK = "pink", "Pink"
        TEAL = "teal", "Teal"
        CYAN = "cyan", "Cyan"
        GREEN = "green", "Green"
        AMBER = "amber", "Amber"
        BROWN = "brown", "Brown"

    name = models.CharField(max_length=64, unique=True)
    colour = models.CharField(
        max_length=16,
        choices=Colour.choices,
        default=Colour.GRAY,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    @property
    def colour_class(self):
        return f"label-{self.colour}"
