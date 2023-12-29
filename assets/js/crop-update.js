import "../scss/tom-select.scss";

window.htmx = require("htmx.org");
// The following is necessary to load Hyperscript. See https://github.com/bigskysoftware/_hyperscript/issues/162
window._hyperscript = require('hyperscript.org');
window._hyperscript.browserInit();

import TomSelect from "tom-select";

const plantspecies = JSON.parse(
  document.getElementById("plantspecies").textContent
);
const speciesID = document.getElementById("id_species").value;
const varietyID = document.getElementById("id_variety").value;

var getVarieties = function (id) {
    let url = id ? `/api/varieties?format=json&species=${id}` : "/api/varieties";
    fetch(url)
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
    valueField: "id",
    labelField: "name",
    searchField: ["name"],
    maxItems: 1,
    create: false,
});

getVarieties(document.getElementById("id_species").value);
