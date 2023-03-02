from typing import List

from calculator.models import Crop
import time
import datetime
import os
import pandas as pd


class CropModel:
    # TODO: AUTOMATICALLY GET PARAMETERS AND ASSIGN TO MODEL PROPERTIES
    inputs: List[str] = []
    inputs_optional: List[str] = []
    context_name = "unnamed_model"
    model_name = "Unnamed Model"
    measure_unit = ""

    def __init__(self, crop: Crop):
        self.object = crop
        self.parameters = self.object.parameters.all()
        self.area = self.object.area

    def can_run(self):
        available_params = list(
            self.object.parameters.values_list("parameter__code", flat=True)
        )
        available_params = available_params + list(
            self.object.species.parameters.values_list("parameter__code", flat=True)
        )
        if self.object.has_variety():
            available_params = available_params + list(
                self.object.variety.species.parameters.values_list(
                    "parameter__code", flat=True
                )
            )
        return all(x in available_params for x in set(self.inputs))

    def has_area(self):
        return self.area.total_area > 0

    def has_weather(self):
        """
        TODO: this method will check if weather is availble for the crop
        """
        if os.path.exists("raw_data/weather.csv"):
            return True
        else:
            return False

    def get_weather_data(self):
        if self.has_weather():
            # Read CSV data. This will change in the future e.g. with a method
            # to retrieve the weather data associated with the Location. This
            # should be in the abstract class
            weather_data = pd.read_csv(
                "raw_data/weather.csv", index_col="date", parse_dates=True
            )
            # Filter only necessary columns, and only selected year
            weather_data = pd.DataFrame(
                weather_data, columns=["tave", "tmin", "tmax", "rad"]
            )[weather_data.index.year == self.year]
            return weather_data
        else:
            return None

    def get_parameter(self, code):
        param = self.object.parameters.filter(parameter__code=code)
        if param.exists():
            return param.last().value
        if self.object.has_variety():
            param = self.object.variety.parameters.filter(parameter__code=code)
            if param.exists():
                return param.last().value
        param = self.object.species.parameters.filter(parameter__code=code)
        if param.exists():
            return param.last().value
        return None

    def output(self):
        context = {}
        context["model_name"] = self.model_name
        context["measure_unit"] = self.measure_unit
        return context

class ModelBasePlots:
    def __init__(self, year: int):
        self.year = year

    def get_base_range_bar_plot(self):
        base_range_bar_plot = {
            "chart": {
                "id": "pheno-dates",
                "height": 250,
                "type": "rangeBar",
                "group": "phenology",
            },
            "plotOptions": {
                "bar": {
                    "horizontal": True,
                    "distributed": True,
                    "dataLabels": {"hideOverflowingLabels": False},
                }
            },
            "dataLabels": {
                "enabled": True,
                "style": {"colors": ["#f3f4f5", "#fff"]},
            },
            "yaxis": {
                "labels": {
                    "minWidth": 40,
                },
            },
            "xaxis": {"show": False},
            "grid": {"row": {"colors": ["#f3f4f5", "#fff"], "opacity": 1}},
            "theme": {"palette": "palette3"},
            "stroke": {"width": 1},
        }
        return base_range_bar_plot

    def get_base_area_plot(self):
        base_area_plot = {
            "chart": {
                "id": "temp-response",
                "type": "area",
                "stacked": False,
                "height": 120,
                "group": "phenology",
                "toolbar": {"show": False},
            },
            "yaxis": {
                "labels": {
                    "minWidth": 40,
                },
                "reversed": True,
                "min": 0,
                "max": 1,
                "tickAmount": 4,
            },
            "dataLabels": {"enabled": False},
            "grid": {"yaxis": {"lines": {"show": False}}},
        }
        return base_area_plot

    def set_plot_xaxis(self, plot_options):
        min_date = datetime.date.fromisoformat(f"{self.year - 1}-12-31")
        max_date = datetime.date.fromisoformat(f"{self.year + 1}-01-01")
        plot_options["xaxis"] = {
            "type": "datetime",
            "min": self.datetime_to_epoch(min_date),
            "max": self.datetime_to_epoch(max_date),
        }
        return plot_options

    def datetime_to_epoch(self, date):
        epoch = time.mktime(date.timetuple()) * 1000
        return int(epoch)
