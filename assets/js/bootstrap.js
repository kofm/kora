import "../scss/bootstrap.scss";
import * as Popper from "@popperjs/core";
import * as bootstrap from "bootstrap";
import TomSelect from "tom-select";

window.TomSelect = TomSelect;

document.addEventListener("DOMContentLoaded", function () {

  // Initialize Bootstrap tooltips
  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach((el) => {
    new bootstrap.Tooltip(el);
  });

  // Initialize TomSelect with data-ts="select"
  document.querySelectorAll('[data-ts="select"]').forEach((el) => {
    new TomSelect(el);
  });

  // Listen for custom event to close modal
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
