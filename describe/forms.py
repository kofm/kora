import csv
import os
import io
import re
from tempfile import NamedTemporaryFile
from django import forms
from django.core.exceptions import MultipleObjectsReturned
from django.db import IntegrityError, transaction
from django.forms import formset_factory
from django.forms import inlineformset_factory
from django.forms.formsets import BaseFormSet
from django.forms.models import BaseInlineFormSet
from django.shortcuts import get_object_or_404
from django.utils.html import format_html
from dynamic_forms import DynamicField, DynamicFormMixin

from register.models import PlantVariety

from .models import Description, Expression, Protocol, Trait, State


class TraitForm(forms.Form):
    numeric_id = forms.IntegerField(required=True)
    description = forms.CharField(required=True)
    protocol_id = forms.IntegerField(widget=forms.HiddenInput)


class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = (
            "numeric_id",
            "description",
        )
        labels = {
            "numeric_id": "Note N°",
            "description": "Note description",
        }


StateFormset = inlineformset_factory(
    Trait,
    State,
    form=StateForm,
    extra=1,
    fields=(
        "numeric_id",
        "description",
    ),
)


class BaseTraitFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_labels = {}
        self.custom_labels["numeric_id"] = "Characteristic N°"
        self.custom_labels["description"] = "Characteristic description"
        for form in self.forms:
            form.fields["numeric_id"].label = self.custom_labels["numeric_id"]
            form.fields["description"].label = self.custom_labels["description"]

    def add_fields(self, form, index):
        form.nested = StateFormset(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            prefix="state-%s-%s" % (form.prefix, StateFormset.get_default_prefix()),
        )
        return super().add_fields(form, index)

    def is_valid(self):
        result = super(BaseTraitFormSet, self).is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, "nested"):
                    result = result and form.nested.is_valid()

        return result

    def empty_form(self):
        form = super().empty_form
        form.fields["numeric_id"].label = self.custom_labels["numeric_id"]
        form.fields["description"].label = self.custom_labels["description"]
        return form

    def save(self, commit=True):

        result = super(BaseTraitFormSet, self).save(commit=commit)

        for form in self.forms:
            if hasattr(form, "nested"):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)

        return result


TraitFormSet = inlineformset_factory(
    Protocol,
    Trait,
    formset=BaseTraitFormSet,
    extra=1,
    fields=(
        "numeric_id",
        "description",
        "grouping",
    ),
)


class ExpressionUpdateForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput())
    state = forms.ModelChoiceField(queryset=State.objects.all())

    def __init__(self, *args, **kwargs):
        super(ExpressionUpdateForm, self).__init__(*args, **kwargs)
        self.fields["state"].required = False
        self.fields["id"].required = False


class DescriptionFilterForm(forms.Form):
    """
    This is the single unit of the form to filter descriptions.
    It needs to be instantiated with a trait id to populate the available states of expression field.
    """

    trait = forms.IntegerField(widget=forms.HiddenInput())
    state = forms.ModelMultipleChoiceField(queryset=None, required=False)

    def __init__(self, *args, **kwargs):
        super(DescriptionFilterForm, self).__init__(*args, **kwargs)
        trait = Trait.objects.get(pk=self.initial["trait"])
        self.fields["state"].queryset = State.objects.filter(trait=trait)
        # self.fields["state"].label = format_html(str(trait.numeric_id) + ". " + trait.description)
        if trait.grouping:
            self.fields["state"].label = format_html(
                f"<b>{trait.numeric_id}. {trait.description}</b>"
            )
        else:
            self.fields["state"].label = format_html(
                f"{trait.numeric_id}. {trait.description}"
            )


class BaseDescriptionFilterFormset(BaseFormSet):
    def save(self):
        filter = list()
        for form in self.forms:
            if states := form.cleaned_data["state"]:
                filter.append(
                    {
                        "trait": form.cleaned_data["trait"],
                        "state": [state.pk for state in states],
                    }
                )
        return filter


DescriptionFilterFormSet = formset_factory(
    DescriptionFilterForm, formset=BaseDescriptionFilterFormset, extra=0
)


class ProtocolForm(forms.Form):
    protocol = forms.ModelChoiceField(queryset=Protocol.objects.all())


def _choices(form, model, depends_on):
    value = form[depends_on].value()
    if value:
        return model.objects.filter(**{depends_on: value})
    else:
        return model.objects.none()


class ProtocolNameForm(forms.ModelForm):
    class Meta:
        model = Protocol
        fields = ("name",)


class RelatedStateForm(DynamicFormMixin, forms.Form):
    def protocol_choices(form):
        state = form["state"].value()
        state = State.objects.get(pk=state)
        protocol = state.trait.protocol
        return Protocol.objects.filter(plantspecies=protocol.plantspecies).exclude(
            pk=protocol.pk
        )

    state = forms.IntegerField(widget=forms.HiddenInput())

    protocol = DynamicField(
        forms.ModelChoiceField,
        queryset=protocol_choices,
    )
    trait = DynamicField(
        forms.ModelChoiceField,
        queryset=lambda form: _choices(form, Trait, "protocol"),
    )
    related_state = DynamicField(
        forms.ModelChoiceField, queryset=lambda form: _choices(form, State, "trait")
    )


class DescriptionForm(forms.Form):
    variety = forms.ModelChoiceField(
        queryset=PlantVariety.objects.all(),
        required=True,
        label="Variety",
        label_suffix="",
    )
    protocol = forms.CharField(label="Protocol", label_suffix="")
    name = forms.CharField(label="Source")

    def save(self):
        data = self.cleaned_data
        variety = data["variety"]
        protocol = Protocol.objects.get(pk=data["protocol"])
        description = Description(variety=variety, protocol=protocol, name=data["name"])
        description.save()
        return description


class DescriptionImportForm(forms.Form):
    protocol = forms.ModelChoiceField(queryset=Protocol.objects.all())
    csv_file = forms.FileField(
        label="CSV file", widget=forms.FileInput(attrs={"accept": "text/csv"})
    )

    def clean_csv_file(self):
        csv_file = self.cleaned_data["csv_file"]
        if csv_file.content_type != "text/csv":
            raise forms.ValidationError("File must be in CSV format.")

        protocol = self.cleaned_data["protocol"]
        if not protocol:
            raise forms.ValidationError("You should provide a valid protocol")
        traits_list = protocol.traits_list()

        chunk = next(csv_file.chunks())
        bytes_io = io.BytesIO(chunk)
        reader = csv.reader(io.TextIOWrapper(bytes_io, encoding="utf-8"))
        header_row = next(reader)
        required_columns = ["variety_name", "description_name"] + [
            f'nchar{trait["numeric_id"]}' for trait in traits_list
        ]
        for column in required_columns:
            if column not in header_row:
                raise forms.ValidationError(
                    f"The file should contain a column named '{column}'"
                )
        if len(list(reader)) > 50:
            raise forms.ValidationError(
                "The maximum number of descriptions to be imported per upload is 50."
            )

        # Write the uploaded file to temp file
        data_file = NamedTemporaryFile()
        with data_file as destination:
            for chunk in csv_file.chunks():
                destination.write(chunk)
            data_file.seek(os.SEEK_SET, os.SEEK_END)

            with open(data_file.name) as csv_file:
                csv_rows = list(csv.DictReader(csv_file))

        return csv_rows

    def save(self):
        """
        This form is responsible for getting the uploaded CSV file and create a
        dictionary to be used with ExpressionFormSet.
        """
        csv_rows = self.cleaned_data["csv_file"]
        protocol = self.cleaned_data["protocol"]
        traits_states_list = protocol.traits_states_list()
        multiple_objects_returned = list()

        # Init formset data
        expression_formset_data = {
            "form-TOTAL_FORMS": len(csv_rows),
            "form-INITIAL_FORMS": 0,
        }

        for nrow, row in enumerate(csv_rows):
            form_id = f"form-{nrow}"

            try:
                variety = PlantVariety.objects.get(
                    name=row["variety_name"], species=protocol.plantspecies
                )
                expression_formset_data.update({f"{form_id}-variety_id": variety.pk})
                expression_formset_data.update({f"{form_id}-variety": variety.name})

            except PlantVariety.DoesNotExist:
                expression_formset_data.update({f"{form_id}-variety": row["variety_name"]})

            except MultipleObjectsReturned:
                multiple_objects_returned.append(
                    {"form": nrow, "variety_name": row["variety_name"]}
                )

            expression_formset_data.update({f"{form_id}-description_name": row["description_name"]})
            expression_formset_data.update({f"{form_id}-protocol": protocol.pk})

            for trait in traits_states_list:
                key = f"{form_id}-expression-trait-{trait['pk']}"
                col_name = f"nchar{trait['numeric_id']}"
                value = row[col_name]
                expression_formset_data.update({key: value})

        return expression_formset_data, multiple_objects_returned, traits_states_list


class ExpressionForm(forms.Form):
    variety = forms.CharField(widget=forms.TextInput(attrs={"class": "ts"}))
    variety_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    protocol = forms.IntegerField(widget=forms.HiddenInput)
    description_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    def __init__(self, *args, traits, **kwargs):
        self.traits = traits
        super(ExpressionForm, self).__init__(*args, **kwargs)

    def clean_variety(self):
        variety = self.cleaned_data["variety"]
        if variety == "":
            raise forms.ValidationError("Variety name can't be empty")
        return variety

    def clean_description_name(self):
        description_name = self.cleaned_data["description_name"]
        variety_id = self.cleaned_data["variety_id"]
        if variety_id:
            protocol = self.cleaned_data["protocol"]
            if Description.objects.filter(
                name=description_name, protocol=protocol, variety__pk=variety_id
            ).exists():
                raise forms.ValidationError(
                    f"A description named {description_name} already exists for this variety."
                )
        return description_name

    def save(self):
        form_data = self.cleaned_data
        protocol = get_object_or_404(Protocol, pk=form_data["protocol"])
        expression_data = {
            key: form_data[key]
            for key in filter(lambda k: k.startswith("expression-trait"), form_data)
        }
        try:
            with transaction.atomic():
                description_kwargs = {
                    "name": form_data["description_name"],
                    "protocol": protocol,
                }
                # This prevents fetching the PlantVariety record if it isn't
                # being created If there is no "variety_id" in the form, then
                # the PlantVariety should be created
                if form_data["variety_id"]:
                    description_kwargs.update({"variety_id": form_data["variety_id"]})
                else:
                    variety = PlantVariety.objects.create(
                        name=form_data["variety"], species=protocol.plantspecies
                    )
                    description_kwargs.update({"variety": variety})

                # Create the description
                description = Description.objects.create(**description_kwargs)

                expressions_kwargs = list()
                for key, val in expression_data.items():
                    if val:
                        trait_id = int(re.search(r"\d+", key).group())
                        state_id = [
                            state["pk"]
                            for item in self.traits
                            if item["pk"] == trait_id
                            for state in item["states"]
                            if state["numeric_id"] == int(val)
                        ]
                        expressions_kwargs.append(
                            {"description": description, "state_id": state_id[0]}
                        )
                Expression.objects.bulk_create(
                    [
                        Expression(**expression_kwargs)
                        for expression_kwargs in expressions_kwargs
                    ]
                )
        except IntegrityError:
            pass


class BaseExpressionFormset(forms.BaseFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        for trait in form.traits:
            form_name = f"expression-trait-{trait['pk']}"
            empty_choice = [("", "-")]
            choices = [
                (state["numeric_id"], state["state_description"]) for state in trait["states"]
            ]
            form.fields[form_name] = forms.ChoiceField(
                choices=empty_choice + choices,
                required=False,
                widget=forms.Select(attrs={"class": "form-select"}),
            )
            form.fields[
                form_name
            ].label = f"{trait['numeric_id']}. {trait['description']}"


ExpressionFormSet = forms.formset_factory(ExpressionForm, formset=BaseExpressionFormset)
