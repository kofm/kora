const value = JSON.parse(document.getElementById('plot-data').textContent);

var options = {
  series: [ { data: value } ],
  legend: {
    show: false
  },
  chart: {
    height: 350,
    type: 'treemap'
  },
  title: {
    text: 'Crops overview'
  }
};
var chart = new ApexCharts(document.querySelector("#treeplot"), options);
chart.render();
