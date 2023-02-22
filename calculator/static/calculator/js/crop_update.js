function getPlotData() {
  let plotData = JSON.parse(document.getElementById("plot-data").textContent);
  return plotData;
}

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
  return plot
}

var plots = []

const plotData = getPlotData();
// htmx.onLoad(function(content) {
//   if (plots) {
//     var plotData = JSON.parse(document.getElementById("plot-data").textContent);
//     plots.forEach(function(value, key) {
//       // value.updateSeries(plotData[key].series)
//       value.destroy()
//     })
//   }
  for (var i in plotData) {
    plots.push(renderPlot(plotData[i], plotData[i].chart.id))
  }
// })
