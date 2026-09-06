from django import forms
from django.forms.widgets import DateInput, HiddenInput
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy

from calculator.models import (
    Crop,
    CropLayout,
    FieldBook,
    Management,
    ManagementType,
    ParameterObservation,
    ParameterTarget,
    Step,
    TraitObservation,
    TraitTarget,
)
from calculator.utils import get_crop_params_list
from describe.models import Protocol, State, Trait
from frontpage.forms import TomSelectModelFormMixin
from frontpage.widgets import BootstrapNumberInput, ModelTomSelect, TomSelect, TomSelectConfig
from parameters.models import Parameter
from register.models import PlantSpecies, PlantVariety
from spaces.models import Location


class ObservationParameterForm(forms.ModelForm):
    class Meta:
        model = ParameterObservation
        fields = ("parameter", "parameter_value", "parameter_date", "notes")
        widgets = {"parameter": TomSelect, "parameter_date": DateInput(attrs={"type": "date"})}


class ParameterObservationUpdateForm(forms.ModelForm):
    class Meta:
        model = ParameterObservation
        fields = ("parameter_value", "parameter_date", "notes")
        widgets = {"parameter_date": DateInput(attrs={"type": "date"})}


class ParameterTargetObservationForm(forms.ModelForm):
    class Meta:
        model = ParameterObservation
        fields = ("parameter", "parameter_value", "parameter_date", "notes")
        widgets = {
            "parameter": HiddenInput,
            "parameter_value": forms.NumberInput(
                attrs={"class": "form-control form-control-lg", "placeholder": "Enter value"}
            ),
            "parameter_date": DateInput(attrs={"class": "form-control form-control-lg", "type": "date"}),
            "notes": forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Notes"}),
        }

    def __init__(self, *args, parameter=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.parameter_obj = parameter
        self.delete_url = None


class TraitObservationInStepCreateForm(forms.ModelForm):
    class Meta:
        model = TraitObservation
        fields = ("state", "notes")


class TraitObservationCreateForm(TomSelectModelFormMixin, forms.ModelForm):
    species = forms.IntegerField(widget=HiddenInput, disabled=True)
    protocol = forms.ModelChoiceField(
        queryset=Protocol.objects.none(),
        widget=ModelTomSelect(
            ts_config=TomSelectConfig(
                url=reverse_lazy("describe:protocol_autocomplete"),
                value_field="id",
                label_field="name",
                search_field="name",
                depends_on="species",
                depends_param="plantspecies_id",
            )
        ),
    )
    trait = forms.ModelChoiceField(
        queryset=Trait.objects.none(),
        widget=ModelTomSelect(
            ts_config=TomSelectConfig(
                url=reverse_lazy("describe:trait_autocomplete"),
                value_field="id",
                label_field="text",
                search_field=["numeric_id", "description"],
                depends_on="protocol",
                depends_param="protocol_id",
            )
        ),
    )
    state = forms.ModelChoiceField(
        queryset=State.objects.none(),
        widget=ModelTomSelect(
            ts_config=TomSelectConfig(
                url=reverse_lazy("describe:state_autocomplete"),
                value_field="id",
                label_field="text",
                search_field=["numeric_id", "description"],
                depends_on="trait",
                depends_param="trait_id",
            )
        ),
    )

    class Meta:
        model = TraitObservation
        fields = ("species", "protocol", "trait", "state", "notes")
        widgets = {"notes": forms.TextInput(attrs={"class": "form-control"})}

    def __init__(self, *args, crop, **kwargs):
        initial = kwargs.setdefault("initial", {})
        initial["species"] = crop.variety.species_id
        super().__init__(*args, **kwargs)
        self.fields["protocol"].queryset = Protocol.objects.filter(plantspecies_id=crop.variety.species_id)


class TraitObservationUpdateForm(forms.ModelForm):
    state = forms.ModelChoiceField(queryset=State.objects.none())

    class Meta:
        model = TraitObservation
        fields = ("state", "notes")
        widgets = {"notes": forms.TextInput(attrs={"class": "form-control"})}


class TraitTargetObservationForm(forms.Form):
    state = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={"class": "form-select form-select-lg"}),
    )
    notes = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-lg"}), required=False)

    def __init__(self, *args, states, protocol=None, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [("", "--------")]
        if states:
            choices += [(state.pk, str(state)) for state in states]
        self.delete_url = None
        self.fields["state"].choices = choices
        self.protocol = protocol


class ManagementTypeForm(forms.ModelForm):
    class Meta:
        model = ManagementType
        fields = ("code", "name", "description")


def get_form_initial_value(form: forms.Form, key: str) -> str:
    field = form.initial.get(key, None)
    # Sometimes a list is used instead of a single value
    return field[0] if isinstance(field, list) else field


def get_parameter_value(form: forms.Form) -> int | None:
    parameter = get_form_initial_value(form, "parameter")
    crop_id = get_form_initial_value(form, "crop")
    if parameter and crop_id:
        crop = get_object_or_404(Crop, pk=crop_id)
        cropparams = get_crop_params_list(crop)
        for param in filter(lambda x: x["parameter"] == int(parameter), cropparams):
            return param["value"]
    return None


class ManagementForm(forms.ModelForm):
    class Meta:
        model = Management
        fields = ("type", "date", "notes")
        widgets = {"date": DateInput(attrs={"type": "date"})}


class CropManagementForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"].label = self.initial["type"].name

    class Meta:
        model = Management
        fields = ("date", "type")
        widgets = {"date": DateInput(attrs={"type": "date"}), "type": HiddenInput()}


class CropLayoutForm(forms.ModelForm):
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        widget=ModelTomSelect(
            ts_config=TomSelectConfig(
                url=reverse_lazy("spaces:location_autocomplete"),
                value_field="id",
                label_field="name",
                search_field="name",
            )
        ),
    )

    class Meta:
        model = CropLayout
        fields = ("name", "location", "ncol", "description")


class InLocationCropLayoutForm(forms.ModelForm):
    class Meta:
        model = CropLayout
        fields = ("name", "ncol", "description")


class CropModelForm(TomSelectModelFormMixin, forms.ModelForm):
    species = forms.ModelChoiceField(
        queryset=PlantSpecies.objects.all(),
        widget=ModelTomSelect(
            ts_config=TomSelectConfig(
                url=reverse_lazy("register:plantspecies_autocomplete"),
                value_field="id",
                label_field="common_name",
                search_field=["common_name", "latin_name"],
            )
        ),
    )
    variety = forms.ModelChoiceField(
        queryset=PlantVariety.objects.none(),
        widget=ModelTomSelect(
            ts_config=TomSelectConfig(
                url=reverse_lazy("register:variety_autocomplete"),
                value_field="id",
                label_field="name",
                search_field="name",
                depends_on="species",
                depends_param="species_id",
            )
        ),
    )

    class Meta:
        model = Crop
        fields = ("species", "variety", "layout", "notes")

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance")
        if instance and instance.variety_id:
            initial = kwargs.setdefault("initial", {})
            initial.setdefault("species", instance.variety.species_id)
        super().__init__(*args, **kwargs)


class CropUpdateForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ("variety", "notes")
        widgets = {"variety": TomSelect}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["variety"].queryset = PlantVariety.objects.filter(species_id=self.instance.variety.species_id)


class FieldBookCreateForm(TomSelectModelFormMixin, forms.ModelForm):
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        widget=ModelTomSelect(
            ts_config=TomSelectConfig(
                url=reverse_lazy("spaces:location_autocomplete"),
                value_field="id",
                label_field="name",
                search_field="name",
            )
        ),
    )
    layout = forms.ModelChoiceField(
        queryset=CropLayout.objects.none(),
        widget=ModelTomSelect(
            ts_config=TomSelectConfig(
                url=reverse_lazy("calculator:croplayout_autocomplete"),
                value_field="id",
                label_field="name",
                search_field="name",
                depends_on="location",
                depends_param="location_id",
            )
        ),
    )

    class Meta:
        model = FieldBook
        fields = ("name", "location", "layout")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["layout"].queryset = self.fields["layout"].queryset.visible()


class InLayoutFieldBookCreateForm(forms.ModelForm):
    class Meta:
        model = FieldBook
        fields = ("name",)


class FieldBookUpdateForm(forms.ModelForm):
    class Meta:
        model = FieldBook
        fields = ("name",)


class StepCropForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ("crop", "order")
        widgets = {"crop": TomSelect}

    def __init__(self, *args, queryset, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["crop"].queryset = queryset


class TraitChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj) -> str:
        return f"({obj.protocol}) {str(obj)} "


class TraitTargetForm(TomSelectModelFormMixin, forms.ModelForm):
    protocol = forms.ModelChoiceField(
        queryset=Protocol.objects.all(),
        widget=ModelTomSelect(
            ts_config=TomSelectConfig(
                url=reverse_lazy("describe:protocol_autocomplete"),
                value_field="id",
                label_field="name",
                search_field="name",
            )
        ),
    )
    trait = TraitChoiceField(
        label="Trait to observe",
        queryset=Trait.objects.none(),
        widget=ModelTomSelect(
            ts_config=TomSelectConfig(
                url=reverse_lazy("describe:trait_autocomplete"),
                value_field="id",
                label_field="text",
                search_field=["numeric_id", "description"],
                depends_on="protocol",
                depends_param="protocol_id",
            ),
            attrs={"placeholder": "Choose a trait"},
        ),
    )

    class Meta:
        model = TraitTarget
        fields = ("protocol", "trait")


class StepUpdateOrderForm(forms.Form):
    start_corner = forms.ChoiceField(
        choices=[
            (None, "Starting corner"),
            ("NW", "North-west"),
            ("NE", "North-east"),
            ("SW", "South-west"),
            ("SE", "South-east"),
        ],
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Starting corner",
    )
    block_width = forms.IntegerField(
        label="Crops per step",
        min_value=1,
        widget=BootstrapNumberInput,
    )
    plot_order = forms.ChoiceField(
        choices=[
            ("left_first", "Left-first"),
            ("right_first", "Right-first"),
        ],
        initial="left_first",
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Plot order",
    )


class ParameterTargetForm(forms.ModelForm):
    class Meta:
        model = ParameterTarget
        fields = ("parameter",)
        labels = {"parameter": "Parameter to record"}
        widgets = {"parameter": TomSelect(attrs={"placeholder": "Choose a parameter"})}


class FieldBookDisplayForm(forms.Form):
    display_config = forms.ChoiceField(
        label="Value shown on plots",
        choices=[],
        widget=forms.Select(attrs={"class": "form-select"}),
        required=False,
    )

    def __init__(self, *args, fieldbook: FieldBook, **kwargs):
        super().__init__(*args, **kwargs)

        self.fieldbook = fieldbook
        url = reverse("calculator:fieldbook_detail_display", args=(fieldbook.pk,))
        self.fields["display_config"].widget.attrs.update({"hx-post": url})

        choices = [(None, "None")]
        traits = Trait.objects.filter(traittarget__step__fieldbook_id=fieldbook.pk).distinct()
        choices += [(f"trait:{trait.pk}:value", f"{trait}") for trait in traits]
        parameters = Parameter.objects.filter(parametertarget__step__fieldbook_id=fieldbook.pk).distinct()
        for parameter in parameters:
            choices += [
                (f"parameter:{parameter.pk}:{field}", f"{parameter.name} ({field.capitalize()})")
                for field in ("value", "date")
            ]
        self.fields["display_config"].choices = choices

    def save(self):
        val = self.cleaned_data.get("display_config")
        if val is None or val == "":
            self.fieldbook.display_config = None
            self.fieldbook.save()
            return self.fieldbook
        model, _id, field = val.split(":")
        self.fieldbook.set_display_config(model, int(_id), field)
        self.fieldbook.save()
        return self.fieldbook
