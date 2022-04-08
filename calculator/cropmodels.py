from calculator.models import Crop
import math
import time
import pandas as pd


class CropModel:
    inputs_crop = []
    context_name = "unnamed_model"
    model_name = "Unnamed Model"
    measure_unit = ""

    def __init__(self, crop: Crop):
        self.object = crop
        self.parameters = self.object.cropparameter_set.all()
        self.area = self.object.area

    def can_run(self):
        available_params_crop = [p.parameter.code for p in self.parameters]
        return all(x in available_params_crop for x in self.inputs_crop)

    def has_area(self):
        return self.area.total_area > 0

    def get_parameter(self, code):
        return self.parameters.get(parameter__code=code).value

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
        context["value"] = result
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
        context["value"] = result
        return context


class PhenologyCropModel(CropModel):
    inputs_crop = ["Tbase", "Topt", "Thigh", "GDDmat"]
    context_name = ["phenology"]
    model_name = "Phenology"

    def output(self):
        context = super().output()
        tbase = self.get_parameter("Tbase")
        topt = self.get_parameter("Topt")
        thigh = self.get_parameter("Thigh")
        gddmat = self.get_parameter("GDDmat")
        # Read CSV data. This will change in the future e.g. with a method
        # to retrieve the weather data associated with the Location
        w = pd.read_csv("weather.csv", index_col="date", parse_dates=True)
        # Filter only necessary columns, and only year 2015
        w = pd.DataFrame(w, columns=["tave", "tmin", "tmax", "rad"])[
            w.index.year == 2015
        ]
        # Exclude days with tave outside the cardinal temperatures range (tbase - thigh)
        tr = w.tave[(w.tave > tbase) & (w.tave < thigh)]
        # Calculate r
        w["r"] = ((thigh - tr) / (thigh - topt) * (tr - tbase) / (topt - tbase)) ** (
            (topt - tbase) / (thigh - topt)
        )
        w["gdd"] = w.r * (topt - tbase)
        w["r"] = w.r.rolling(window=30, min_periods=1).mean()
        w["sowing"] = w.r > 0.2
        start, end = w[w.r > 0.2].index[[0, -1]]
        start = w.index.get_loc(start)
        end = w.index.get_loc(end)
        mat_dates = []
        sow_dates = []
        for i in range(start, end):
            t = w.iloc[i:].copy()
            t.gdd = t.gdd.cumsum()
            try:
                mat_date = t[t.gdd - gddmat > 0].index[0]
                if t.loc[mat_date]["r"] > 0.2:
                    mat_dates.append(mat_date)
                    sow_dates.append(t.index[0])
            except:
                pass
        if len(mat_dates) > 1 and len(sow_dates) > 1:
            w["maturity"] = pd.Series(True, index=pd.Series(mat_dates).unique())
            w["sowing"] = w.sowing & pd.Series(True, index=sow_dates)
            context = {}
            context["timeseries"] = {
                "data": [
                    {
                        "x": "Sowing",
                        "y": [
                            # datetime.strftime(d, "%Y-%m-%d")
                            time.mktime(d.timetuple()) * 1000
                            for d in w[w.sowing == True].index[[0, -1]]
                        ],
                        "fillcolor": "#008FFB",
                    },
                    {
                        "x": "Maturity",
                        "y": [
                            # datetime.strftime(d, "%Y-%m-%d")
                            time.mktime(d.timetuple()) * 1000
                            for d in w[w.maturity == True].index[[0, -1]]
                        ],
                        "fillcolor": "#00E396",
                    },
                ]
            }
            context["temp_response"] = {
                "data": [
                    {"x": time.mktime(x.timetuple()) * 1000, "y": round(y, 2)}
                    for x, y in zip(w.index, w.r.fillna(0))
                ]
            }
        else:
            context["timeseries"] = {"data": []}
        return context
