from frontpage.widgets import TomSelectLabel, TomSelectLabelMultiple


class DescriptionLabelSelectMixin:
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
        if value:
            label = value.instance
            colour = label.colour_class
            option["attrs"]["data-colour"] = colour

        return option


class DescriptionLabelSelect(DescriptionLabelSelectMixin, TomSelectLabel):
    pass


class DescriptionLabelSelectMultiple(DescriptionLabelSelectMixin, TomSelectLabelMultiple):
    pass
