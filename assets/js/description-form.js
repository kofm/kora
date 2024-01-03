// JS logic to populate the tom-select inputs in Description forms
// Mind that the protocol restapi endpoint is stored in a `url`
// variable assigned in the description_form.html template

import '../scss/tom-select.scss'
import TomSelect from 'tom-select'

const sources = JSON.parse(document.getElementById('sources').textContent)

const varietyTomSelect = new TomSelect('#id_variety', {
	maxItems: 1,
	create: false,
})

const protocolTomSelect = new TomSelect('#id_protocol', {
	maxItems: 1,
	create: false,
	valueField: 'pk',
	labelField: 'name',
	searchField: ['name'],
})

new TomSelect('#id_name', {
	options: sources,
	maxItems: 1,
	create: true,
	persist: false,
})

function getProtocols(id) {
	if (!id) {
		protocolTomSelect.disable()
		return
	}

	let protocol = protocolTomSelect.getValue()

	fetch(`${url}&variety=${id}`)
		.then((response) => response.json())
		.then((data) => {
			protocolTomSelect.clear()
			protocolTomSelect.clearOptions()
			protocolTomSelect.addOptions(data)
			protocolTomSelect.enable()
			if (protocol) {
				protocolTomSelect.setValue(protocol)
			}
		})
}

varietyTomSelect.on('change', getProtocols)

let variety = varietyTomSelect.getValue()

if (variety) {
	getProtocols(variety)
} else {
	protocolTomSelect.disable()
}
