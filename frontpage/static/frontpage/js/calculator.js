var endpoint = $("#area_select").attr("data-url");
var area_select = document.getElementById('area_select')
var plantspecies_select = document.getElementById('plantspecies_select')

function getArea() {
  const areaId = $('#area_select').val();  // get the selected subject ID from the HTML dropdown list
  const plantspeciesId = $('#plantspecies_select').val();  // get the selected subject ID from the HTML dropdown list
  $.ajax({                       // initialize an AJAX request
    type: "POST",
    url: endpoint,
    data: {
      'area_id': areaId,       // add the country id to the POST parameters
      'plantspecies_id': plantspeciesId,       // add the country id to the POST parameters
      'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),
    },
    success: function (data) {   // `data` is from `get_topics_ajax` view function
      d=JSON.parse(data)
      var w = d[0].fields.width
      var l = d[0].fields.length
      var area = w * l
      var yield = d[1].fields.value
      $("#dimensions_card").html(w + " x " + l + " m <br> (" + Math.round(area, 1) + " m<sup>2</sup>)"); // replace the contents of the topic input with the data that came from the server
      $("#yield_card").html(Math.round(yield * area) + "<br>kg (" + yield + " kg/m<sup>2</sup>)"); // replace the contents of the topic input with the data that came from the server
    }
  });
}

$(document).ready(function() {
  getArea();
  area_select.addEventListener('change', getArea);
  plantspecies_select.addEventListener('change', getArea);
})
