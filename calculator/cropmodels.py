from calculator.models import Crop
import math
import time
import datetime
import pandas as pd


class CropModel:
    inputs_crop = []
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
            self.object.content_object.parameters.values_list(
                "parameter__code", flat=True
            )
        )
        if self.object.has_variety():
            available_params = available_params + list(
                self.object.content_object.species.parameters.values_list(
                    "parameter__code", flat=True
                )
            )
        return all(x in available_params for x in set(self.inputs_crop))

    def has_area(self):
        return self.area.total_area > 0

    def get_parameter(self, code):
        param = self.object.parameters.filter(parameter__code=code).last()
        if not param:
            param = self.object.content_object.parameters.filter(
                parameter__code=code
            ).last()
        if not param and self.object.has_variety():
            param = self.object.content_object.species.parameters.filter(
                parameter__code=code
            ).last()
        return param.value

    def output(self):
        context = {}
        context["model_name"] = self.model_name
        context["measure_unit"] = self.measure_unit
        return context


class CropModelExpectedYield(CropModel):
    inputs_crop = [
        "yield",
    ]
    context_name = "expected_yield"
    model_name = "Expected yield"
    measure_unit = "kg"

    def can_run(self):
        return super().can_run() & self.has_area()

    def output(self):
        context = super().output()
        result = self.get_parameter("yield") * self.area.total_area
        context["value"] = int(result)
        return context


class CropModelTotalPlants(CropModel):
    inputs_crop = [
        "distw",
        "distb",
    ]
    context_name = "total_plants"
    model_name = "Total plants"

    def can_run(self):
        return super().can_run() & self.has_area()

    def output(self):
        context = super().output()
        nrow = math.floor(self.object.area.width / self.get_parameter("distb"))
        ncol = math.floor(1 / self.get_parameter("distw"))
        result = round(ncol * nrow * self.area.total_area, 0)
        context["value"] = int(result)
        return context


class PhenologyCropModel(CropModel):
    inputs_crop = ["Tbase", "Topt", "Thigh", "GDDmat"]
    context_name = "phenology"
    model_name = "Phenology"

    def __init__(self, crop: Crop, year: int = 2016, rmin: float = 0.4):
        super().__init__(crop)
        self.year = year
        self.rmin = rmin

    def get_weather_data(self):
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

    def temp_response(self, t, tbase, topt, thigh):
        """
        Function to calculate the temperature response according to Yan, Weikai
        and Hunt, Leslie A "An Equation for Modelling the Temperature Response
        of Plants using only the Cardinal Temperatures" Annals of Botany (1999)
        """
        r = ((thigh - t) / (thigh - topt) * (t - tbase) / (topt - tbase)) ** (
            (topt - tbase) / (thigh - topt)
        )
        return r

    def get_base_range_bar_plot(self):
        base_range_bar_plot = {
            "chart": {
                "id": "pheno-dates",
                "height": 150,
                "type": "rangeBar",
                "group": "phenology",
                "toolbar": {"show": False},
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
            "yaxis": [
                {
                    "show": False,
                    "showAlways": False,
                    "tooltip": {"enabled": False, "offsetX": 0},
                    "crosshairs": {
                        "show": True,
                        "position": "front",
                        "stroke": {"color": "#b6b6b6", "width": 1, "dashArray": 0},
                    },
                }
            ],
            "grid": {"row": {"colors": ["#f3f4f5", "#fff"], "opacity": 1}},
            "annotations": {"yaxis": [], "xaxis": [], "points": []},
        }
        return base_range_bar_plot

    def get_base_area_plot(self):
        base_area_plot = {
            "chart": {
                "id": "temp-response",
                "type": "area",
                "stacked": False,
                "height": 250,
                "group": "phenology",
            },
            "yaxis": {
                "labels": {
                    "minWidth": 40,
                },
            },
            "dataLabels": {"enabled": False},
            "markers": {
                "size": 0,
            },
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

    def get_datetime_range_to_epoch(self, dates_list):
        dates_range = [min(dates_list), max(dates_list)]
        dates_range = [self.datetime_to_epoch(date) for date in dates_range]
        return dates_range

    def output(self):
        context = super().output()
        tbase = self.get_parameter("Tbase")
        topt = self.get_parameter("Topt")
        thigh = self.get_parameter("Thigh")
        gddmat = self.get_parameter("GDDmat")
        weather_data = self.get_weather_data()
        # Exclude days with tave outside the cardinal temperatures range (tbase - thigh)
        tr = weather_data.tave[
            (weather_data.tave > tbase) & (weather_data.tave < thigh)
        ]
        weather_data["r"] = self.temp_response(tr, tbase, topt, thigh)
        # Calculate GDDs
        weather_data["gdd"] = weather_data.r * (topt - tbase)
        # Smooth temperature response
        weather_data["r"] = weather_data.r.rolling(window=30, min_periods=1).mean().fillna(0)
        # Define the range of usable temperatures based on a threshold
        r_range = weather_data.r > self.rmin
        maturity_dates = []
        sowing_dates = []
        for date in weather_data[r_range].index:
            t = weather_data.loc[date:].copy()
            t.gdd = t.gdd.cumsum()
            try:
                maturity_date = t[t.gdd - gddmat > 0].index[0]
                if t.loc[maturity_date].r > self.rmin:
                    sowing_dates.append(date)
                    maturity_dates.append(maturity_date)
            except:
                pass
        plot_pheno_dates = self.get_base_range_bar_plot()
        plot_pheno_dates = self.set_plot_xaxis(plot_pheno_dates)
        plot_temp_response = self.get_base_area_plot()
        plot_temp_response = self.set_plot_xaxis(plot_temp_response)

        if len(maturity_dates) > 1:
            sowing_range = self.get_datetime_range_to_epoch(sowing_dates)
            maturity_range = self.get_datetime_range_to_epoch(maturity_dates)
            # Date range plot
            plot_pheno_dates["series"] = [
                {
                    "data": [
                        {
                            "x": "Sowing",
                            "y": sowing_range,
                            "fillcolor": "#008FFB",
                        },
                        {
                            "x": "Maturity",
                            "y": maturity_range,
                            "fillcolor": "#00E396",
                        },
                    ]
                }
            ]
            # Temperature reponse plot
        else:
            plot_pheno_dates["serie"] = [{ "data": []}]

        plot_temp_response["series"] = [
            {
                "data": [
                    {"x": self.datetime_to_epoch(x), "y": round(y, 2)} for x, y in zip(weather_data.index, weather_data.r)
                ],
            }
        ]
        context["plots"] = [plot_pheno_dates, plot_temp_response]
        return context
