// JS logic to populate the tom-select inputs in Description forms
// Mind that the protocol restapi endpoint is stored in a `url`
// variable assigned in the description_form.html template

import "../scss/tom-select.scss";
import TomSelect from "tom-select";

const sources = JSON.parse(document.getElementById("sources").textContent);
let protocolTomSelect;

const getProtocols = (id) => {

    if (!protocolTomSelect) {
	return;
    }

    if (!id) {
	protocolTomSelect.disable();
	return;
    }

    fetch(`${url}&variety=${id}`)
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
    onChange: getProtocols,
});

protocolTomSelect = new TomSelect("#id_protocol", {
    maxItems: 1,
    create: false,
    valueField: "pk",
    labelField: "name",
    searchField: ["name"],
    onInitialize: () => getProtocols(varietyTomSelect.getValue()),
});

new TomSelect("#id_name", {
    options: sources,
    maxItems: 1,
    create: true,
    persist: false,
});
