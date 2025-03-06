/******/ (() => { // webpackBootstrap
/*!****************************************!*\
  !*** ./assets/js/plantvariety-form.js ***!
  \****************************************/
const speciesInput = document.getElementById("id_species");
const breederInput = document.getElementById("id_breeder");

if (speciesInput) {
    new TomSelect(speciesInput);
}

if (breederInput) {
    new TomSelect(breederInput);
}

/******/ })()
;