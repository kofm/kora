/* ==================
 * Bootstrap helpers
 * ================== */

export function initializeTooltips(root = document) {
    if (!window.bootstrap) return;
    root.querySelectorAll('[data-bs-toggle="tooltip"]').forEach((el) => {
        new window.bootstrap.Tooltip(el);
    });
}

export function closeModalById(modalId = "modal") {
    if (!window.bootstrap) return;
    const el = document.getElementById(modalId);
    if (!el) return;
    let modal = window.bootstrap.Modal.getInstance(el);
    if (!modal) modal = new window.bootstrap.Modal(el);
    modal.hide();
}

export function initializeToast(element) {
    if (!window.bootstrap) return;
    let toast = window.bootstrap.Toast.getInstance(element);
    if (!toast) {
        toast = new window.bootstrap.Toast(element);
        toast.show();
    } else if (!toast.isShown()) {
        toast.dispose();
        element.remove();
    }
}
