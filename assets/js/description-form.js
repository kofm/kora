import "../scss/tom-select.scss";
import TomSelect from "tom-select";
const sources = JSON.parse(document.getElementById("sources").textContent);
const protocols = JSON.parse(document.getElementById("protocols").textContent);

var getProtocols = function (id) {
  fetch("/species/" + id + "/protocols")
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
  options: protocols,
  maxItems: 1,
  create: false,
  valueField: "pk",
  labelField: "name",
  searchField: ["name"],
});

new TomSelect("#id_name", {
  options: sources,
  maxItems: 1,
  create: true,
  persist: false,
});

if(!varietyTomSelect.getValue()) {
  console.log("Not set")
  protocolTomSelect.disable();
}
