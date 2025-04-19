import "../scss/bootstrap.scss";
import * as Popper from "@popperjs/core";
import * as bootstrap from "bootstrap";
import TomSelect from "tom-select";

window.TomSelect = TomSelect;

function initializeTomSelects(root = document) {
  root.querySelectorAll('.tomselect').forEach((el) => {
    // If already initialized and still attached, skip
    if (el.tomselectInstance && el.tomselectInstance.wrapper.parentNode) {
      return;
    }

    // If previously broken instance exists, destroy it
    if (el.tomselectInstance) {
      el.tomselectInstance.destroy();
    }

    const options = {};

    // Dynamically map data-ts-* attributes into options
    for (const attr of el.attributes) {
      if (attr.name.startsWith('data-ts-')) {
        const optionName = attr.name
          .replace('data-ts-', '')
          .replace(/-([a-z])/g, (_, char) => char.toUpperCase());

        let value = attr.value;

        if (value === 'true') {
          value = true;
        } else if (value === 'false') {
          value = false;
        } else if (!isNaN(value) && value.trim() !== '') {
          value = Number(value);
        }

        options[optionName] = value;
      }
    }

    el.tomselectInstance = new TomSelect(el, options);
  });
}

document.addEventListener("DOMContentLoaded", function () {

  // Initialize Bootstrap tooltips
  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach((el) => {
    new bootstrap.Tooltip(el);
  });

  // Initialize TomSelects
  initializeTomSelects();

  // Reinitialize after HTMX swaps
  document.body.addEventListener('htmx:afterSwap', (event) => {
    initializeTomSelects(event.target);
  });

  // Handle modal close event
  document.body.addEventListener('closeModal', function() {
    const modalElement = document.getElementById("modal");
    if (modalElement) {
      let modal = bootstrap.Modal.getInstance(modalElement);
      if (!modal) {
        modal = new bootstrap.Modal(modalElement);
      }
      modal.hide();
    }
  });

});
