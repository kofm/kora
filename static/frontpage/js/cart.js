const alertBox = document.getElementById("alert-box");

function changeWeight(element) {
  let formdata = new FormData(element.parentElement);
  fetch(element.getAttribute("data-url"), {
    method: "POST",
    body: formdata,
  })
    .then((response) => {
      alertBox.style.display = "none";
      if (!response.ok) {
        element.value = element.max;
        return response.json();
      }
    })
    .then((data) => {
      if (data) {
        alertBox.style.display = "block";
        alertBox.textContent = data["__all__"];
      }
    })
    .catch((error) => {
      console.error("Error: ", error);
    });
}

function changeWeightSelected(weight) {
  Array.from(document.querySelectorAll("td input[type=checkbox]:checked")).map(
    (elem) => {
      let input = elem.closest("tr").querySelector("input[type=number]")
      input.value = weight;
      changeWeight(input);
  });
}
