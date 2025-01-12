from datetime import date

from django_countries.fields import CountryField

from django.db import models
from django.urls.base import reverse
from django.utils.html import format_html
from frontpage.generic import ModelIsDeletableMixin

INDIVIDUAL = "IN"
PARTNERSHIP = "PA"
COMPANY = "CO"
COOPERATIVE = "CP"
ENTITY_TYPE_CHOICES = (
    (INDIVIDUAL, "Individual"),
    (PARTNERSHIP, "Partnership"),
    (COMPANY, "Company"),
    (COOPERATIVE, "Cooperative"),
)
PBR = "PBR"
NLI = "NLI"
CAT = "CAT"
PROTECTION_TYPE_CHOICES = (
    (PBR, "Plant Breeders' Rights"),
    (NLI, "National Listing"),
    (CAT, "Common Catalogue"),
)
PROTECTION_STATUS_CHOICES = (
    ("G", "Granted"),
    ("T", "Terminated"),
    ("A", "Active Application"),
    ("W", "Withdrawn"),
    ("R", "Refused"),
    ("S", "Surrendered"),
)


class Entity(ModelIsDeletableMixin, models.Model):
    name = models.CharField(max_length=200, help_text="Name of the entity. E.g., 'John Doe', 'Doe & Partners', etc.")
    type = models.CharField(
        max_length=2,
        choices=ENTITY_TYPE_CHOICES,
        blank=True,
        default="",
        help_text="Type of the entity. Choose from the available options.",
    )
    country = CountryField(blank=True, null=True, help_text="Country where the entity is based or operates.")
    contact = models.CharField(
        max_length=500,
        blank=True,
        default="",
        help_text="Contact details of the entity, such as phone number or address.",
    )
    email = models.EmailField(default="", help_text="Email address of the entity. E.g., 'john.doe@example.com'.")

    class Meta:
        ordering = ("name",)
        verbose_name = "entity"
        verbose_name_plural = "entities"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("register:entity_detail", args=(self.pk,))

    def get_delete_url(self):
        return reverse("register:entity_delete", args=(self.pk,))


class PlantSpecies(ModelIsDeletableMixin, models.Model):
    common_name = models.CharField(max_length=100, unique=True)
    latin_name = models.CharField(max_length=100)
    plant_types = (
        ("tree", "Tree"),
        ("shrub", "Shrub"),
        ("vegetable", "Vegetable"),
        ("herbaceous", "Herbaceous"),
    )
    plant_type = models.CharField(max_length=100, choices=plant_types)

    class Meta:
        ordering = ("common_name",)
        verbose_name = "plant species"
        verbose_name_plural = "plant species"

    def __str__(self):
        return format_html("{} (<i>{}</i>)", self.common_name, self.latin_name)

    def get_absolute_url(self):
        return reverse("register:plantspecies_detail", args=[self.pk])

    @property
    def total_descriptions(self):
        return self.variety.filter(description__isnull=False).count()

    @property
    def total_seedsamples(self):
        return self.variety.filter(seedsample__isnull=False).count()

    def get_update_url(self):
        return reverse("register:plantspecies_update", args=[self.pk])

    def get_list_url(self):
        return reverse("register:plantspecies_list")

    def get_delete_url(self):
        return reverse("register:plantspecies_delete", args=[self.pk])


class PlantVariety(ModelIsDeletableMixin, models.Model):
    name = models.CharField(help_text="The name of the variety", max_length=100)
    species = models.ForeignKey(PlantSpecies, on_delete=models.PROTECT, related_name="variety")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    breeder = models.ForeignKey(Entity, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "variety"
        verbose_name_plural = "varieties"

    def __str__(self):
        return f"{self.name} ({self.species.common_name})"

    def get_absolute_url(self):
        return reverse("register:plantvariety_detail", args=[self.pk])

    def get_list_url(self):
        return reverse("register:variety_list")

    def get_delete_url(self):
        return reverse("register:variety_delete", args=[self.pk])

    def other_names(self):
        return self.names.exclude(name=self.name)

    def has_breeder(self):
        return bool(self.breeder)


class PlantVarietyName(models.Model):
    name = models.CharField(max_length=200)
    variety = models.ForeignKey(PlantVariety, on_delete=models.CASCADE, related_name="names")
    change_date = models.DateField(blank=True, null=True, default=date.today)

    class Meta:
        ordering = ("-change_date",)
        verbose_name = "denomination"
        verbose_name_plural = "denominations"

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("register:plantvariety_detail", args=[self.variety.pk])

    def get_delete_url(self):
        return reverse("register:denomination_delete", args=[self.pk])

    def is_deletable(self):
        return self.variety.names.count() > 1


class Protection(ModelIsDeletableMixin, models.Model):
    type = models.CharField(max_length=3, choices=PROTECTION_TYPE_CHOICES)
    status = models.CharField(max_length=1, blank=True, default="", choices=PROTECTION_STATUS_CHOICES)
    country = CountryField(null=True)
    variety = models.ForeignKey(PlantVariety, on_delete=models.CASCADE)
    reference = models.CharField(max_length=100, blank=True, default="")
    applicants = models.ManyToManyField(Entity, related_name="applicants", blank=True)
    maintainers = models.ManyToManyField(Entity, blank=True)
    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)
    note = models.CharField(max_length=512, blank=True, help_text="Add any additional information here.")

    class Meta:
        ordering = ("-date_start",)

    def __str__(self) -> str:
        return f"{self.type} for {self.variety.name}"

    def get_absolute_url(self):
        return reverse("register:protection_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("register:protection_update", args=(self.pk,))

    def get_delete_url(self):
        return reverse("register:protection_delete", args=(self.pk,))
