// JS logic to populate the tom-select inputs in Description forms
// Mind that the protocol restapi endpoint is stored in a `url`
// variable assigned in the description_form.html template

import "../scss/tom-select.scss";
import TomSelect from "tom-select";

const varietyTomSelect = new TomSelect("#id_variety", {
    maxItems: 1,
    create: false,
});

new TomSelect("#id_name", {
    maxItems: 1,
    create: true,
    persist: false,
});

var protocol = document.getElementById('id_protocol');

if(protocol) {
    const protocolTomSelect = new TomSelect("#id_protocol", {
	maxItems: 1,
	create: false,
	valueField: "pk",
	labelField: "name",
	searchField: ["name"],
    });


    function getProtocols(id) {
	if (!id) {
	    protocolTomSelect.disable();
	    return;
	}

	let protocol = protocolTomSelect.getValue();

	fetch(`${url}&variety=${id}`)
	    .then((response) => response.json())
	    .then((data) => {
		protocolTomSelect.clear();
		
		protocolTomSelect.addOptions(data);
		protocolTomSelect.enable();
		if (protocol) {
		    protocolTomSelect.setValue(protocol);
		}
	    });
    }

    varietyTomSelect.on("change", getProtocols);

    let variety = varietyTomSelect.getValue();

    if (variety) {
	getProtocols(variety);
    } else {
	protocolTomSelect.disable();
    }

}
