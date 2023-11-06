// JS logic to populate the tom-select inputs in Description forms
// Mind that the protocol restapi endpoint is stored in a `url`
// variable assigned in the description_form.html template
import "../scss/tom-select.scss";
import TomSelect from "tom-select";
const sources = JSON.parse(document.getElementById("sources").textContent);

var getProtocols = function (id) {
    if (!id) {
	protocolTomSelect.disable();
	return;
    }
    fetch(url + "&variety=" + id)
    .then((response) => response.json())
    .then((data) => {
        protocolTomSelect.clear();
        protocolTomSelect.clearOptions();
        protocolTomSelect.addOptions(data);
        protocolTomSelect.enable();
    });
};

const varietyTomSelect = new TomSelect("#id_variety", {
    maxItems: 1,
    create: false,
    onChange: function (value) {
	getProtocols(value);
    },
});

const protocolTomSelect = new TomSelect("#id_protocol", {
    maxItems: 1,
    create: false,
    valueField: "pk",
    labelField: "name",
    searchField: ["name"],
    onInitialize: function() {
	this.disable();
    }
});

new TomSelect("#id_name", {
    options: sources,
    maxItems: 1,
    create: true,
    persist: false,
});
