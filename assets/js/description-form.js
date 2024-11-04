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
    items: []
});

const protocol = document.getElementById("id_protocol");

if (protocol) {
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

        const protocolValue = protocolTomSelect.getValue();

        fetch(`${url}&variety=${id}`)
            .then((response) => response.json())
            .then((data) => {
                protocolTomSelect.clearOptions(); 
                protocolTomSelect.addOptions(data);
                protocolTomSelect.refreshOptions(); 
                protocolTomSelect.enable(); 
                
                if (protocolValue) {
                    protocolTomSelect.setValue(protocolValue);
                }
            });
    }
    
    varietyTomSelect.on("change", () => getProtocols(varietyTomSelect.getValue()));
    
    const initialVariety = varietyTomSelect.getValue();
    if (initialVariety) {
        getProtocols(initialVariety);
    } else {
        protocolTomSelect.disable();
    }
}
