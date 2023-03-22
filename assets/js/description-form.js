import "../scss/tom-select.scss";
import TomSelect from "tom-select";
const sources = JSON.parse(
  document.getElementById("sources").textContent
);

new TomSelect("#id_name", {
  options: sources,
  maxItems: 1,
  create: true,
  persist: false
});

new TomSelect("#id_variety", {
  maxItems: 1,
  create: false,
  onChange: function (value) {
    getProtocols(value);
  },
});


var getProtocols = function (id) {
  fetch("/register/species/" + id + "/protocols")
    .then((response) => response.json())
    .then((data) => {
      protocolTomSelect.clear();
      protocolTomSelect.clearOptions();
      protocolTomSelect.addOptions(data);
      protocolTomSelect.enable();
    });
};

const protocolTomSelect = new TomSelect("#id_protocol", {
  options: [],
  maxItems: 1,
  create: false,
  valueField: "pk",
  labelField: "name",
  searchField: ["name"],
});
protocolTomSelect.disable()
