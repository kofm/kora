const parameterAddBtn = document.getElementById("parameter-add-btn");
const parameterAddForm = document.getElementById("parameter-add-form");
const parametersList = document.getElementById("parameters-list");

parameterAddBtn.addEventListener("click", async function () {
  const url = parameterAddBtn.getAttribute("data-url");
  let parameterAddFormData = new FormData(parameterAddForm);

  const response = await fetch(url, {
    method: "post",
    headers: {
      Accept: "application/json"
    },
    body: parameterAddFormData
  })

  const newParameter = await response.json();
  if (response.ok) {
    var newLiElement = document.createElement("li");
    newLiElement.id = "cropparam-" + newParameter.id;
    newLiElement.setAttribute("class", "list-group-item");
    newLiElement.appendChild(document.createTextNode(newParameter.parameter_data.name + ": " + newParameter.value + " " + newParameter.parameter_data.measure_unit));
    parametersList.appendChild(newLiElement);
  }
});

async function deleteCropParameter(element) {

  const removedElement = element;
  const url = removedElement.getAttribute("data-url");

  const response = await fetch(url, {
    method: "delete",
    headers: {
      Accept: "application/json"
    }
  });

  if (response.ok) {
    let id = element.parentNode.id
    let liElement = document.getElementById(id);
    parametersList.removeChild(liElement);
  }
}
