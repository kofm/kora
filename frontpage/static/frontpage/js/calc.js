// Form elements
const locationSelect = document.getElementById("location-select");
const areaSelect = document.getElementById("area-select");
const speciesSelect = document.getElementById("species-select");
const varietySelect = document.getElementById("variety-select");
const csrfToken = document.querySelector("input[name=csrfmiddlewaretoken]");

// Dimensions card elements
const areaCardSubtitle = document.getElementById("area-card-subtitle");
const areaWidthSpan = document.getElementById("area-width-span");
const areaLengthSpan = document.getElementById("area-length-span");
const areaTotalSpan = document.getElementById("area-total-span");

// Crop card elements
const cropCardSubtitle = document.getElementById("crop-card-subtitle");
const cropYieldSpan = document.getElementById("yield-span");
const cropExpectedYieldSpan = document.getElementById("expected-yield-span");

const cropDistbInput = document.getElementById("distb-input");
const cropDistwInput = document.getElementById("distw-input");

var areaObjects;
var cropParamDistw, cropParamDistb, cropParamYield;

// Helper functions
// ================

// Simple function to multiply two numbers and round the result
function multiply(wid, len) {
  return Math.round(wid * len, 0);
}

// Function to hide an element by its id.
function hideElement(id) {
  document.getElementById(id).style.display = "none";
}

// Function to show an element by its id.
function showElement(id) {
  document.getElementById(id).style.display = "block";
}

function updateCropCard() {
  cropCardSubtitle.textContent = speciesSelect.selectedOptions[0].text;
  cropYieldSpan.textContent = cropParamYield.fields.value;
  cropDistbInput.value = cropParamDistb.fields.value;
  cropDistwInput.value = cropParamDistw.fields.value;
  cropExpectedYieldSpan.textContent = multiply(
    cropParamYield.fields.value,
    areaTotalSpan.textContent
  );
  showElement("crop-card");
}

// Function to update the displayed card relative to the Area dimensions
function updateDimensionsCard() {
  const selectedArea = areaObjects.find(
    (element) => element.pk == areaSelect.value
  );
  showElement("dimensions-card");
  areaWidthSpan.textContent = selectedArea.fields.width;
  areaLengthSpan.textContent = selectedArea.fields.length;
  areaTotalSpan.textContent = multiply(
    selectedArea.fields.width,
    selectedArea.fields.length
  );
  areaCardSubtitle.textContent =
    "Area " +
    selectedArea["fields"].name +
    " (" +
    locationSelect.selectedOptions[0].text +
    ")";
}

locationSelect.addEventListener("change", async () => {
  hideElement("dimensions-card");
  hideElement("crop-card");

  if (locationSelect.value != "") {
    let formdata = new FormData();
    formdata.append("loc", locationSelect.value);
    formdata.append("csrfmiddlewaretoken", csrfToken.value);

    const url = locationSelect.getAttribute("data-url");

    const response = await fetch(url, {
      method: "POST",
      credentials: "same-origin",
      body: formdata,
    });

    if (response.ok) {
      areaObjects = await response.json();
      // Enables the area select input
      areaSelect.removeAttribute("disabled");
      // Remove previous inputs
      areaSelect.length = 0;
      // Set the first, empty option
      areaSelect.options[0] = new Option("", "");
      // Iterate through AJAX results to populate the area select input
      for (let i = 0; i < areaObjects.length; i += 1) {
        areaSelect.options[areaSelect.length] = new Option(
          areaObjects[i]["fields"].name,
          areaObjects[i]["pk"]
        );
      }
    } else {
      alert("Error");
    }
  } else {
    areaSelect.toggleAttribute("disabled");
    areaSelect.length = 0;
  }
});

// Events that happen when the area select input is changed
areaSelect.addEventListener("change", function () {
  // If the empty value is chosen
  if (areaSelect.value != "") {
    updateDimensionsCard();
    if (speciesSelect.hasAttribute("disabled")) {
      speciesSelect.removeAttribute("disabled");
    } else {
      updateCropCard();
    }
  } else {
    hideElement("dimensions-card");
    speciesSelect.toggleAttribute("disabled");
  }
});

speciesSelect.addEventListener("change", async () => {
  if (speciesSelect.value != "") {
    let formdata = new FormData();
    formdata.append("species", speciesSelect.value);
    formdata.append("csrfmiddlewaretoken", csrfToken.value);

    const url = speciesSelect.getAttribute("data-url");

    const response = await fetch(url, {
      method: "POST",
      credentials: "same-origin",
      body: formdata,
    });

    if (response.ok) {

      // This object contains all the instances fetched from endpoints
      // It contains all the PlantVariety instances associated to the
      // selected species and the last distw, distb, and yield parameters
      fetchedSpeciesInstances = await response.json();

      // Extract only the PlantVariety model instances
      const varietyModelInstances = fetchedSpeciesInstances.filter(
        (element) => element.model == "register.plantvariety"
      );
      cropParamDistw = fetchedSpeciesInstances.filter(
        (element) => element.fields["parameter"] == "distw"
      )[0];
      cropParamDistb = fetchedSpeciesInstances.filter(
        (element) => element.fields["parameter"] == "distb"
      )[0];
      cropParamYield = fetchedSpeciesInstances.filter(
        (element) => element.fields["parameter"] == "yield"
      )[0];
      updateCropCard();
      // Enables the area select input
      varietySelect.removeAttribute("disabled");
      // Remove previous inputs
      varietySelect.length = 0;
      // Set the first, empty option
      varietySelect.options[0] = new Option("", "");
      // Iterate through AJAX results to populate the area select input
      for (let i = 0; i < varietyModelInstances.length; i += 1) {
        varietySelect.options[varietySelect.length] = new Option(
          varietyModelInstances[i]["fields"].name,
          varietyModelInstances[i]["pk"]
        );
      }
    } else {
      alert("Error");
    }
  } else {
    varietySelect.toggleAttribute("disabled");
    varietySelect.length = 0;
  }
});
