var plantspecies_select = document.getElementById('plantspecies_select')

function getVarieties() {
  const plantspeciesId = $('#plantspecies_select').val();  // get the selected subject ID from the HTML dropdown list

  $.ajax({
    type: "POST",
    url: $("#variety").attr("data-url"),
    data: {
      'plantspecies_id': plantspeciesId,
      'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),
    },
    success: function (data) {   // `data` is from `get_topics_ajax` view function
      $('#variety').html("");
      data=JSON.parse(data);
      jQuery.each(data, function(variety) {
        $('#variety').append("<option>" + this.fields.name + "</option>");
      });
    }
  })
}

$(document).ready(function() {
  getVarieties();
  plantspecies_select.addEventListener('change', getVarieties);
})
