from datetime import date
from django.db import models
from django.urls.base import reverse
from django_countries.fields import CountryField


class Entity(models.Model):
    INDIVIDUAL = "IN"
    PARTNERSHIP = "PA"
    COMPANY = "CO"
    COOPERATIVE = "CP"
    ENTITY_TYPE_CHOICES = [
        (INDIVIDUAL, "Individual"),
        (PARTNERSHIP, "Parnership"),
        (COMPANY, "Company"),
        (COOPERATIVE, "Cooperative"),
    ]
    name = models.CharField(max_length=200)
    type = models.CharField(
        max_length=2, choices=ENTITY_TYPE_CHOICES, blank=True, null=True
    )
    country = CountryField(blank=True, null=True)
    contact = models.CharField(max_length=500, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse(
            "register:entity-detail",
            args=[
                self.pk,
            ],
        )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class PlantSpecies(models.Model):
    common_name = models.CharField(max_length=100, unique=True)
    latin_name = models.CharField(max_length=100)
    plant_types = (
        ("tree", "Tree"),
        ("shrub", "Shrub"),
        ("vegetable", "Vegetable"),
        ("herbaceous", "Herbaceous"),
    )
    plant_type = models.CharField(max_length=100, choices=plant_types)

    @property
    def total_descriptions(self):
        return self.variety.filter(description__isnull=False).count()

    @property
    def total_seedsamples(self):
        return self.variety.filter(seedsample__isnull=False).count()

    def __str__(self):
        return self.common_name

    def get_absolute_url(self):
        return reverse("register:plantspecies-detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["common_name"]


class PlantVarietyManager(models.Manager):
    def get_by_species_values_list(self, plantspecies):
        """
        Returns a list of dictionaries containing the PKs and the names of the
        varieties of a particular PlantSpecies
        """
        qs = (
            self.filter(species=plantspecies)
            .prefetch_related("breeder")
            .values("pk", "name", "breeder__name")
        )
        return list(qs)


class PlantVariety(models.Model):
    name = models.CharField(help_text="The name of the variety", max_length=100)
    species = models.ForeignKey(
        PlantSpecies, on_delete=models.PROTECT, related_name="variety"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    breeder = models.ForeignKey(
        Entity, on_delete=models.SET_NULL, null=True, blank=True
    )
    objects = PlantVarietyManager()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "register:plantvariety-detail",
            args=[
                self.pk,
            ],
        )

    def has_breeder(self):
        if self.breeder:
            return True
        else:
            return False


class PlantVarietyName(models.Model):
    name = models.CharField(max_length=200)
    variety = models.ForeignKey(
        PlantVariety, on_delete=models.CASCADE, related_name="names"
    )
    change_date = models.DateField(blank=True, null=True, default=date.today)

    class Meta:
        ordering = [
            "-change_date",
        ]

    def get_absolute_url(self):
        return reverse(
            "register:plantvariety-detail",
            args=[
                self.variety.pk,
            ],
        )


class Protection(models.Model):
    PBR = "PBR"
    NLI = "NLI"
    CAT = "CAT"
    PROTECTION_TYPE_CHOICES = [
        (PBR, "Plant Breeders' Right"),
        (NLI, "National Listing"),
        (CAT, "Common Catalogue"),
    ]
    PROTECTION_STATUS_CHOICES = [
        ("G", "Granted"),
        ("T", "Terminated"),
        ("A", "Active Application"),
        ("W", "Withdrawn"),
        ("R", "Refused"),
    ]
    type = models.CharField(max_length=3, choices=PROTECTION_TYPE_CHOICES)
    status = models.CharField(
        max_length=1, blank=True, null=True, choices=PROTECTION_STATUS_CHOICES
    )
    country = CountryField()
    variety = models.ForeignKey(PlantVariety, on_delete=models.CASCADE)
    reference = models.CharField(max_length=100, blank=True, null=True)
    applicants = models.ManyToManyField(
        Entity,
        related_name="applicants",
        blank=True,
    )
    maintainer = models.ForeignKey(
        Entity,
        on_delete=models.PROTECT,
        related_name="maintainers",
        blank=True,
        null=True,
    )
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse("register:protection-detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-date_start"]

    def __str__(self) -> str:
        return self.get_type_display() + " for " + self.variety.name
