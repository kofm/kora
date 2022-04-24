const plantspecies = JSON.parse(
  document.getElementById("plantspecies").textContent
);
const speciesID = document.getElementById("id_species").value;
const varietyID = document.getElementById("id_variety").value;
var getVarieties = function (id) {
  fetch("/register/species/" + id + "/varieties")
    .then((response) => response.json())
    .then((data) => {
      tsVariety.clear();
      tsVariety.clearOptions();
      tsVariety.addOptions(data);
      if (tsSpecies.getValue() == speciesID) {
        tsVariety.addItem(varietyID);
      }
    });
};

const tsSpecies = new TomSelect("#id_species", {
  options: plantspecies,
  valueField: "pk",
  labelField: "common_name",
  searchField: ["common_name"],
  maxItems: 1,
  create: false,
  onChange: function (value) {
    getVarieties(value);
  },
});

const tsVariety = new TomSelect("#id_variety", {
  options: [],
  valueField: "pk",
  labelField: "names__name",
  searchField: ["names__name"],
  maxItems: 1,
  create: false,
});
getVarieties(document.getElementById("id_species").value);

const plotData = JSON.parse(document.getElementById("plot-data").textContent);

function renderPlot(data, id) {
  let options = data;

  if (options.chart.id == "pheno-dates") {
    options["dataLabels"] = {
      enabled: true,
      formatter: function (val, opts) {
        var label = opts.w.globals.labels[opts.dataPointIndex];
        return label;
      },
      style: {
        colors: ["#f3f4f5", "#fff"],
      },
    };
  }

  if (options.chart.id == "temp-response") {
    options["chart"]["events"] = {
      click: function (event, chartContext, config) {
        // gets the position of the marker in the series
        const dp = config.dataPointIndex;

        // use the series position of the clicked marker to find the corresponding x axis data at that point in the series
        let date = chartContext.data.twoDSeriesX[dp];

        // convert to date
        date = new Date(date);
        date.setYear(2022);

        // update sowing date input
        document.getElementById("id_sowing").value = date
          .toISOString()
          .split("T")[0];
      },
    };
  }


  let plot = new ApexCharts(document.getElementById(id), options);
  plot.render()
}

for (var i in plotData) {
  renderPlot(plotData[i], plotData[i].chart.id)
}
