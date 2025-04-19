import * as bootstrap from "bootstrap";

export function initializeTooltips(root = document) {
    root.querySelectorAll('[data-bs-toggle="tooltip"]').forEach((el) => {
        new bootstrap.Tooltip(el);
    });
}

export function closeModalById(modalId = "modal") {
    const modalElement = document.getElementById(modalId);
    if (modalElement) {
        let modal = bootstrap.Modal.getInstance(modalElement);
        if (!modal) {
            modal = new bootstrap.Modal(modalElement);
        }
        modal.hide();
    }
}
