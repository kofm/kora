const parameterSelect = document.getElementById("parameter-select");
const parameterValueInput = document.getElementById("parameter-value-input");
const searchParameter = what => availableParameters.find(element => element.parameter__id == what);

function getParameter() {
  const selectedParameter = searchParameter(parameterSelect.value);
  if (selectedParameter) {
    parameterValueInput.value = selectedParameter.value;
  } else {
    parameterValueInput.value = "";
  }
}

getParameter();
parameterSelect.addEventListener("change", function () {
  getParameter();
});
