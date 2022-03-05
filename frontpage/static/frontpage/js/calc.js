const loc=document.getElementById("location");
const area=document.getElementById("area");
const csrf=document.querySelector("input[name=csrfmiddlewaretoken]");

var area_result;

function hideDimensions() {
  document.getElementById("dimensions").style.display = "none";
}

function calcArea(wid, len) {
  return Math.round(wid * len, 0);
}

loc.addEventListener('change', async () => {

  hideDimensions();

  if (loc.value != "") {
    let formdata = new FormData();
    formdata.append('loc', loc.value);
    formdata.append('csrfmiddlewaretoken', csrf.value)

    const url=loc.getAttribute("data-url");

    const response = await fetch(url, {
      method: 'POST',
      credentials: 'same-origin',
      body: formdata
    })

    if (response.ok) {
      area_result = await response.json();
      // Enables the area select input
      area.removeAttribute("disabled");
      // Remove previous inputs
      area.length = 0;
      // Set the first, empty option
      area.options[0] = new Option("", "");
      // Iterate through AJAX results to populate the area select input
      for (let i = 0; i < area_result.length; i += 1) {
        area.options[area.length] = new Option(area_result[i]["fields"].name, area_result[i]["pk"])
      }
    } else {
      alert("Error");
    }
  } else {

    area.toggleAttribute("disabled");
    area.length = 0;
  }

});

area.addEventListener('change', function () {
  if (area.value != "") {
    const selarea = area_result.find(function(ar) {
      return ar.pk==area.value;
    });
    document.getElementById("dimensions").style.display = "block";
    document.getElementById("width").textContent = selarea["fields"].width;
    document.getElementById("length").textContent = selarea["fields"].length;
    document.getElementById("total_area").textContent = calcArea(selarea["fields"].width, selarea["fields"].length);
    document.getElementById("areainfo").textContent = "Area " + selarea["fields"].name + " (" + loc.selectedOptions[0].text + ")";
  } else {
    hideDimensions();
  }
});
