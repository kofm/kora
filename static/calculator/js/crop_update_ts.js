const plantspecies = JSON.parse(
  document.getElementById("plantspecies").textContent
);
const speciesID = document.getElementById("id_species").value;
const varietyID = document.getElementById("id_variety").value;
var getVarieties = function (id) {
  fetch("/register/species/" + id + "/varieties")
    .then((response) => response.json())
    .then((data) => {
      tsVariety.clear();
      tsVariety.clearOptions();
      tsVariety.addOptions(data);
      if (tsSpecies.getValue() == speciesID) {
        tsVariety.addItem(varietyID);
      }
    });
};

const tsSpecies = new TomSelect("#id_species", {
  options: plantspecies,
  valueField: "pk",
  labelField: "common_name",
  searchField: ["common_name"],
  maxItems: 1,
  create: false,
  onChange: function (value) {
    getVarieties(value);
  },
});

const tsVariety = new TomSelect("#id_variety", {
  options: [],
  valueField: "pk",
  labelField: "names__name",
  searchField: ["names__name"],
  maxItems: 1,
  create: false,
});
getVarieties(document.getElementById("id_species").value);
