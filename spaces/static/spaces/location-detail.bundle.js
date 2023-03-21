/******/ (() => { // webpackBootstrap
var __webpack_exports__ = {};
/*!**************************************!*\
  !*** ./assets/js/location-detail.js ***!
  \**************************************/
const data = document.currentScript.dataset;
const isSortable = data.sortable === "true";

htmx.onLoad(function (content) {
  var sortableCards = content.querySelectorAll("#grid-area");
  for (var i = 0; i < sortableCards.length; i++) {
    var card = sortableCards[i];
    new Sortable(card, {
      animation: 150,
      sort: isSortable,
    });
  }
});

/******/ })()
;