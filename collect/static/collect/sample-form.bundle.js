/******/ (() => { // webpackBootstrap
/*!**********************************!*\
  !*** ./assets/js/sample-form.js ***!
  \**********************************/
const varietiesData = JSON.parse(
  document.getElementById("varieties-data").textContent
);
const positionsData = JSON.parse(
  document.getElementById("positions-data").textContent
);
const btnAnother = document.getElementById("btn-another");
const varietyHiddenInput = document.getElementById("id_variety");
const positionHiddenInput = document.getElementById("id_position");

document.addEventListener("DOMContentLoaded", function () {
  const varietyInput = document.getElementById("id_variety");
  var config = {
    options: varietiesData,
    valueField: "variety__id",
    labelField: "name",
    searchField: ["name"],
    items: [varietyHiddenInput.value],
    maxItems: 1,
    selectOnTab: true,
    onChange: function (value) {
      varietyHiddenInput.value = value;
    },
  };
  const tomVarInput = new TomSelect("#id_tomvar", config);
  if (varietyHiddenInput.value == "") {
    tomVarInput.focus();
  }

  const positionInput = document.getElementById("id_position");
  var configPos = {
    options: positionsData,
    valueField: "pk",
    labelField: "position_name",
    searchField: ["position_name"],
    // If positionHiddenInput is not set we're in the CreateView, so select the
    // first available position
    // Otherwise select the actual data (we're in UpdateView)
    items: [
      positionHiddenInput.value == ""
        ? positionsData[0].pk
        : positionHiddenInput.value,
    ],
    maxItems: 1,
    selectOnTab: true,
    sortField: [{ field: "$order" }, { field: "$score" }],
    onChange: function (value) {
      positionHiddenInput.value = value;
    },
  };
  new TomSelect("#id_tompos", configPos);
  if (positionHiddenInput.value == "") {
    positionHiddenInput.value = positionsData[0].pk;
  }
});
document.addEventListener(
  "keydown",
  (event) => {
    const keyName = event.key;

    if (event.shiftKey & (keyName === "Enter")) {
      // Even though event.key is not 'Control' (e.g., 'a' is pressed),
      // event.ctrlKey may be true if Ctrl key is pressed at the same time.
      btnAnother.click();
    }
  },
  false
);

/******/ })()
;