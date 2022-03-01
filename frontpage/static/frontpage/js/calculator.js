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
      // d=JSON.parse(data)
      $("#dimensions_card").html(data.width + " x " + data.length + " m <br> (" + data.total_area + " m<sup>2</sup> total area)"); // replace the contents of the topic input with the data that came from the server
      $("#yield_card").html(data.expected_yield + " kg (" + data.yield + " kg/m<sup>2</sup>)"); // replace the contents of the topic input with the data that came from the server
      planting_text = "Total plants: " + data.plant_number + "<br>";
      planting_text += "Planting scheme: " + data.distb + "x" + data.distw + "m";
      planting_text += " (" + data.nrow + " rows)";
      $("#planting_card").html(planting_text);
      // $("#planting_card").html("Total plants: " + data.plant_number + "<br>Rows: " + data.nrow + " rows with " + data.nplants + " plants each row"); // replace the contents of the topic input with the data that came from the server
      $("#distb_select").html(data.distb);
      $("#distb_range").attr('value', data.distb * 100)
      $("#distw_select").html(data.distw);
      $("#distw_range").attr('value', data.distw * 100)
    }
  });
}

function getVarieties() {
  const plantspeciesId = $('#plantspecies_select').val();  // get the selected subject ID from the HTML dropdown list

  $.ajax({
    type: "POST",
    url: $("#plantvariety_select").attr("data-url"),
    data: {
      'plantspecies_id': plantspeciesId,
      'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),
    },
    success: function (data) {   // `data` is from `get_topics_ajax` view function
      $('#plantvariety_select').html("");
      data=JSON.parse(data);
      jQuery.each(data, function(variety) {
        $('#plantvariety_select').append("<option>" + this.fields.name + "</option>");
      });
    }
  })
}

$(document).ready(function() {
  getArea();
  getVarieties();
  area_select.addEventListener('change', getArea);
  plantspecies_select.addEventListener('change', getArea);
  plantspecies_select.addEventListener('change', getVarieties);
})
