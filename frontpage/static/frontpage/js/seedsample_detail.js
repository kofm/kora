const storageSelect = document.getElementById("storage-select");
const storagePositionSelect = document.getElementById(
  "storage-position-select"
);

const sampleForm = document.getElementById("sample-form");
const sampleFormButton = document.getElementById("sample-form-button")

const germinabilityTable = document.getElementById("germinability-table")
const germinabilityValueInput = document.getElementById("germinability-value-input")
const germinabilityDaysInput = document.getElementById("germinability-days-input")
const germinabilityDateInput = document.getElementById("germinability-date-input")
const germinabilityForm = document.getElementById("germinability-form")
const germinabilityButton = document.getElementById("germinability-form-button")


const weightTable = document.getElementById("weight-table")
const weightForm = document.getElementById("weight-form")
const weightValueInput = document.getElementById("weight-value-input")
const weightButton = document.getElementById("weight-form-button")

germinabilityButton.addEventListener("click", async function() {
  const url = germinabilityButton.getAttribute("data-url");
  let germinabilityFormData = new FormData(germinabilityForm);
  const response = await fetch(url, {
    method: "POST",
    headers: {
      Accept: "application/json"
    },
    body: germinabilityFormData
  })

  console.log(response);

  const newGerminability = await response.json();
  console.log(newGerminability);
  let newRow = germinabilityTable.insertRow();
  let valueCell = newRow.insertCell();
  let daysCell = newRow.insertCell();
  let dateCell = newRow.insertCell();
  valueCell.appendChild(document.createTextNode(newGerminability.germinability + " %"));
  daysCell.appendChild(document.createTextNode(newGerminability.after_days));
  dateCell.appendChild(document.createTextNode(newGerminability.performed_at));
});

weightButton.addEventListener("click", async function() {
  const url = weightButton.getAttribute("data-url");
  let weightFormData = new FormData(weightForm);
  const response = await fetch(url, {
    method: "POST",
    headers: {
      Accept: "application/json"
    },
    body: weightFormData
  });

  const newWeight = await response.json();
  let newRow = weightTable.insertRow();
  let valueCell = newRow.insertCell();
  let dateCell = newRow.insertCell();
  valueCell.appendChild(document.createTextNode(newWeight.value));
  dateCell.appendChild(document.createTextNode(newWeight.created_at));
});

sampleFormButton.addEventListener("click", async function() {
  const url = sampleFormButton.getAttribute("data-url");
  let sampleFormData = new FormData(sampleForm);
  const response = await fetch(url, {
    method: "PUT",
    headers: {
      Accept: "application/json"
    },
    body: sampleFormData
  });

  const updatedSample = await response.json();
  console.log(updatedSample);
});
