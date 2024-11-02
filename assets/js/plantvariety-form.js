import "../scss/tom-select.scss";
import TomSelect from "tom-select";

const speciesInput = document.getElementById("id_species");
const breederInput = document.getElementById("id_breeder");

if (speciesInput) {
    new TomSelect(speciesInput);
}

if (breederInput) {
    new TomSelect(breederInput);
}
