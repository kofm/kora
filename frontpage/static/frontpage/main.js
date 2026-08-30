import { initializeTomSelects } from "./tomselect.js";
import { closeModalById, initializeToast, initializeTooltips } from "./bootstrap.js";
import { initializeSortableElements } from "./sortable.js";
import { initializeCoordinateGrids } from "./grid.js";

const copyIdFeedbackDuration = 1500;
let copyIdFeedbackTimeout;

async function copyDetailPageId(button) {
    const rawId = button.dataset.copyId;
    const status = button.querySelector("[data-copy-id-status]");

    try {
        await navigator.clipboard.writeText(rawId);
    } catch {
        return;
    }

    window.clearTimeout(copyIdFeedbackTimeout);
    document.querySelectorAll(".detail-page-id-badge.is-copied").forEach((badge) => {
        badge.classList.remove("is-copied");
        const badgeStatus = badge.querySelector("[data-copy-id-status]");
        if (badgeStatus) badgeStatus.textContent = "";
    });

    button.classList.add("is-copied");
    if (status) status.textContent = `ID ${rawId} copied`;

    copyIdFeedbackTimeout = window.setTimeout(() => {
        button.classList.remove("is-copied");
        if (status) status.textContent = "";
    }, copyIdFeedbackDuration);
}

function handleDetailPageIdClick(event) {
    const button = event.target.closest("[data-copy-id]");
    if (!button) return;
    copyDetailPageId(button);
}

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
    initializeCoordinateGrids(document);

    document.addEventListener("click", handleDetailPageIdClick);
    document.body.addEventListener("closeModal", () => closeModalById("modal"));
});

if (window.htmx) {
    registerTomSelectExtension(window.htmx);

    document.addEventListener("htmx:beforeCleanupElement", (event) => {
        event.detail.elt.querySelectorAll?.(".grid-layout-coordinate-wrapper").forEach((wrapper) => {
            wrapper._coordinateCleanup?.();
        });
    });

    document.addEventListener("htmx:afterSwap", () => {
        initializeSortableElements(document);
        initializeCoordinateGrids(document);
    });

    window.htmx.onLoad(() => {
        window.htmx.findAll(".toast").forEach((el) => initializeToast(el));
    });
}
