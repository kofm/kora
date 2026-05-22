import { initializeTomSelects } from "./tomselect.js";
import { closeModalById, initializeToast, initializeTooltips } from "./bootstrap.js";
import { initializeSortableElements } from "./sortable.js";

function registerTomSelectExtension(htmx) {
    if (!htmx || !window.TomSelect) return;
    htmx.defineExtension("tomselect", {
        onEvent: function (name, evt) {
            if (name === "htmx:beforeSwap") {
                const elt = evt.detail.target;
                if (elt) {
                    elt.querySelectorAll("select.tomselect").forEach((el) => {
                        if (el._tomselectCleanup) el._tomselectCleanup();
                        if (el.tomselect) el.tomselect.destroy();
                    });
                }
            }
            if (name === "htmx:afterSettle") {
                const elt = evt.detail.elt;
                if (elt) {
                    initializeTomSelects(elt);
                }
            }
        },
    });
}

document.addEventListener("DOMContentLoaded", () => {
    initializeTooltips();
    initializeTomSelects();
    initializeSortableElements(document);

    document.body.addEventListener("closeModal", () => closeModalById("modal"));
});

if (window.htmx) {
    registerTomSelectExtension(window.htmx);

    document.addEventListener("htmx:afterSwap", () => {
        initializeSortableElements(document);
    });

    window.htmx.onLoad(() => {
        window.htmx.findAll(".toast").forEach((el) => initializeToast(el));
    });
}
