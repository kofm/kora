import ApexCharts from 'apexcharts'

const sampleWeights = JSON.parse(
  document.getElementById('sample-weights').textContent
);
var options = {
        series: [{
                name: "Sample weight",
                data: sampleWeights,
              }],
        chart: {
                height: 350,
                type: 'line',
                zoom: {
                        enabled: false
                      }
              },
        dataLabels: {
                enabled: false
              },
        stroke: {
                curve: 'straight'
              },
        title: {
                text: 'Sample weight over time',
                align: 'left'
              },
        xaxis: {
                type: 'datetime'
              }
      };

var chart = new ApexCharts(document.querySelector("#sampleweight-chart"), options);
chart.render();
