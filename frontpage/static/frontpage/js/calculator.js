var endpoint = $("#area_select").attr("data-url");
var area_select = document.getElementById('area_select')
var plantspecies_select = document.getElementById('plantspecies_select')

function getArea() {

  // Prepare POST data
  const post_data = {
    // get the selected area ID from the HTML select input
    'area_id': $('#area_select').val(),
    // get the selected plantspecies ID from the HTML select input
    'plantspecies_id': $('#plantspecies_select').val(),
    // add CSRF token
    'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),
  }

  // initialize an AJAX request
  $.ajax({
    type: "POST",
    url: endpoint,
    data: post_data,
    success: function (data) {

      if (data.distb == null) {
        data.distb = 0;
        data.distw = 0;
      }

      // Change area data
      $("#width").html(data.width);
      $("#length").html(data.length);
      $("#total_area").html(Math.round(data.width*data.length,0));

      // Change Crop data
      $("#expected_yield").html(data.expected_yield);
      $("#yield").html(data.yield);
      $("#plant_number").html(data.plant_number);
      $("#distb").html(data.distb);
      $("#distw").html(data.distw);
      $("#nrow").html(data.nrow);

      // Change range inputs for planting scheme
      $("#distb_select").html(data.distb);
      $('#distb_range').val(data.distb*100);
      $("#distw_select").html(data.distw);
      $('#distw_range').val(data.distw*100);
    }
  });
}

function getVarieties() {
  $.ajax({
    type: "POST",
    url: $("#plantvariety_select").attr("data-url"),
    data: {
      'plantspecies_id': $('#plantspecies_select').val(),
      'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),
    },
    success: function (data) {
      $('#plantvariety_select').html("<option></option>");
      data=JSON.parse(data);
      // Iterate through returned list of varieties
      jQuery.each(data, function(variety) {
        $('#plantvariety_select').append("<option>" + this.fields.name + "</option>");
      });
    }
  })
}

function get_plants_number(distb, distw, width=1) {
  if (distb==0 || distw==0) {
    return {
      nrow: 0,
      ncol: 0,
      plants: 0
    };
  }

  var nrow=Math.floor(width/distb);
  nrow=nrow < 2 ? 1 : nrow;
  var ncol=Math.floor(1/distw);
  ncol=ncol < 2 ? 1 : ncol;
  return {
    nrow: nrow,
    ncol: ncol,
    plants: nrow*ncol
  };
}

$(document).ready(function() {
  getArea();
  getVarieties();
  area_select.addEventListener('change', getArea);
  plantspecies_select.addEventListener('change', getArea);
  plantspecies_select.addEventListener('change', getVarieties);

  document.getElementById('distw_range').addEventListener('input', function (){
    $("#distw_select").html($("#distw_range").val());

  });
  document.getElementById('distb_range').addEventListener('input', function (){

    var new_val=$("#distb_range").val()/100;
    var distb=$('#distw_range').val()/100;
    var len=$("#length").text();
    var wid=$("#width").text();

    var planting_scheme=get_plants_number(distb, new_val, wid);
    console.log(planting_scheme);

    $("#distb_select").html(new_val);

    $("#plant_number").html(planting_scheme.plants);
    // $("#expected_yield").html(data.expected_yield);
    // $("#yield").html(data.yield);
    // $("#distb").html(data.distb);
    // $("#distw").html(data.distw);
    $("#nrow").html(planting_scheme.nrow);
  });
})
