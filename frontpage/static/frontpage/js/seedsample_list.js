const varietySearchInput = document.getElementById("variety-search-input");
// document.addEventListener("DOMContentLoaded", async function () {
//   const url = "http://localhost:8000/api/seedsample";
//   const response = await fetch(url, {
//     headers: {
//       Accept: "application/json",
//     },
//   });
//   varietiesObject = await response.json();
//   console.log(varietiesObject);
//   var config = {
//     options: varietiesObject,
//     valueField: "id",
//     labelField: "variety",
//     searchField: ["id", "variety", "notes", "position", "growing_season"],
//   };
//   new TomSelect("#variety-search-input", config);
// });
//
// varietySearchInput.addEventListener("keyup", function () {
//   console.log(varietySearchInput.value);
//   console.log(result);
// });

var select = new TomSelect("#variety-search-input", {
  valueField: "id",
  labelField: "variety",
  searchField: ["id", "variety", "notes", "position", "growing_season"],
  // fetch remote data
  load: function (query, callback) {
    var self = this;
    if (self.loading > 1) {
      callback();
      return;
    }

    const url = "http://localhost:8000/api/seedsample";
    fetch(url)
      .then((response) => response.json())
      .then((json) => {
        callback(json);
        self.settings.load = null;
      })
      .catch(() => {
        callback();
      });
  },
});

select.on("change", function () {
  const url = varietySearchInput
    .getAttribute("data-url")
    .replace("0", varietySearchInput.value);
  window.open(url);
});
