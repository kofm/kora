// Import our custom CSS
import "../scss/bootstrap.scss";

// Import all of Bootstrap's JS
import * as Popper from "@popperjs/core";
import * as bootstrap from "bootstrap";

document.addEventListener("DOMContentLoaded", function () {
  const tooltipTriggerList = document.querySelectorAll(
    '[data-bs-toggle="tooltip"]'
  );

  const tooltipList = [...tooltipTriggerList].map(
    (tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl)
  );
});

import TomSelect from "tom-select";
window.TomSelect = TomSelect;
