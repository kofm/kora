// Formatter for the labels of date range plot.
function dateRangePlotFormatter(val, opts) {
  var label = opts.w.globals.labels[opts.dataPointIndex];
  return label;
}

// Handler for the click event on the plot
function clickEventHandler(event, chartContext, config) {
  // gets the position of the marker in the series
  const dp = config.dataPointIndex;
  // use the series position of the clicked marker to find the corresponding x
  // axis data at that point in the series
  let date = chartContext.data.twoDSeriesX[dp];
  // convert to date
  date = new Date(date);
  // change the year to the current year
  let current_year = new Date().getFullYear()
  date.setYear(current_year);
  // update sowing date input
  document.getElementById("id_sowing").value = date.toISOString().split("T")[0];
}

// Get JSON data passed from Django view
const plotData = JSON.parse(document.getElementById("plot-data").textContent);

// Function to render all the plots contained in plotData, which is returned by Django view
function renderPlot(data, id) {

  let options = data;

  // Add the formatter to the pheno-dates plot
  if (options.chart.id == "pheno-dates") {
    options["dataLabels"] = {
      formatter: dateRangePlotFormatter,
    };
  }

  // Add the click event handler to the temp-response plot
  if (options.chart.id == "temp-response") {
    options["chart"]["events"] = {
      click: clickEventHandler,
    };
  }
  console.log(options);
  // Create the plot at the specified id
  let plot = new ApexCharts(document.getElementById(id), options);
  // Render the plot
  plot.render();
}

// Loop over all the plots passed from django views
for (var i in plotData) {
  // For each plot data item, render a plot to the div with the same ID
  renderPlot(plotData[i], plotData[i].chart.id);
}
