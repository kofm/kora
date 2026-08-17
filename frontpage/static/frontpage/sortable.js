/* =========
 * Sortable
 * ========= */
export function initializeSortableElements(container = document) {
    if (!window.Sortable) return;
    container.querySelectorAll(".sortable").forEach((element) => {
        if (element._sortable) element._sortable.destroy();
        element._sortable = new window.Sortable(element, {
            animation: 150,
            delay: 250,
            delayOnTouchOnly: true,
            disabled: element.dataset.sortable !== "true",
        });
    });
}

function toggleSortableState(toggle) {
    const target = document.querySelector(toggle.dataset.sortableToggle);
    if (!target?._sortable) return;

    const enabled = target._sortable.option("disabled");
    target._sortable.option("disabled", !enabled);
    target.dataset.sortable = String(enabled);
    toggle.setAttribute("aria-pressed", String(enabled));
    toggle.querySelectorAll("[data-sortable-toggle-label]").forEach((label) => {
        label.hidden = label.dataset.sortableToggleLabel !== (enabled ? "enabled" : "disabled");
    });
}

document.addEventListener("click", (event) => {
    const toggle = event.target.closest("[data-sortable-toggle]");
    if (toggle) toggleSortableState(toggle);
});
