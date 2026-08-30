/* =========
 * Sortable
 * ========= */
const sortableModes = {
    locked: { disabled: true, swap: false },
    reorder: { disabled: false, swap: false },
    swap: { disabled: false, swap: true },
};

export function initializeSortableElements(container = document) {
    if (!window.Sortable) return;
    container.querySelectorAll(".sortable").forEach((element) => {
        if (element._sortable) element._sortable.destroy();
        element._sortable = new window.Sortable(element, {
            animation: 150,
            delay: 250,
            delayOnTouchOnly: true,
            disabled: element.dataset.sortable !== "true",
            swapClass: "border-primary",
            onEnd: (event) => handleSortEnd(event),
        });
    });
    container.querySelectorAll("[data-sortable-mode-control]").forEach(setSortableMode);
    container.querySelectorAll("[data-deferred-sortable-form]").forEach(initializeDeferredSortableForm);
}

function initializeDeferredSortableForm(form) {
    form._sortableOrder = getSortableOrder(form);
}

function getSortableOrder(form) {
    return Array.from(form.querySelectorAll('.sortable [name="order"]'), (input) => input.value);
}

function handleSortEnd(event) {
    if (event.oldIndex === event.newIndex) return;
    const form = event.to.closest("[data-deferred-sortable-form]");
    if (!form) return;
    form.querySelector("[data-sortable-pending-actions]").hidden = false;
}

function setPendingActionsDisabled(form, disabled) {
    form.querySelectorAll("[data-sortable-confirm], [data-sortable-cancel]").forEach((button) => {
        button.disabled = disabled;
    });
}

function getModeControl(form) {
    return document.querySelector(form.dataset.sortableControl);
}

function lockDeferredSortable(form) {
    const control = getModeControl(form);
    if (!control) return;
    control.value = "locked";
    setSortableMode(control);
}

function finishDeferredSort(form) {
    form._sortableOrder = getSortableOrder(form);
    form.querySelector("[data-sortable-pending-actions]").hidden = true;
    setPendingActionsDisabled(form, false);
    const control = getModeControl(form);
    if (control) control.disabled = false;
    lockDeferredSortable(form);
}

function cancelDeferredSort(form) {
    const sortable = form.querySelector(".sortable");
    const itemsById = new Map(
        Array.from(sortable.children, (item) => [item.querySelector('[name="order"]').value, item]),
    );
    form._sortableOrder.forEach((id) => sortable.append(itemsById.get(id)));
    finishDeferredSort(form);
}

function setSortableMode(control) {
    const target = document.querySelector(control.dataset.sortableModeControl);
    const mode = sortableModes[control.value];
    if (!target?._sortable || !mode) return;

    target._sortable.option("disabled", mode.disabled);
    target._sortable.option("swap", mode.swap);
    target.dataset.sortable = String(!mode.disabled);
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

    const cancel = event.target.closest("[data-sortable-cancel]");
    if (cancel) cancelDeferredSort(cancel.closest("[data-deferred-sortable-form]"));
});

document.addEventListener("change", (event) => {
    const control = event.target.closest("[data-sortable-mode-control]");
    if (control) setSortableMode(control);
});

document.addEventListener("htmx:beforeRequest", (event) => {
    const form = event.target.closest("[data-deferred-sortable-form]");
    if (!form) return;
    const control = getModeControl(form);
    form._sortableMode = control?.value;
    if (control) control.disabled = true;
    form.querySelector(".sortable")._sortable.option("disabled", true);
    setPendingActionsDisabled(form, true);
});

document.addEventListener("htmx:afterRequest", (event) => {
    const form = event.target.closest("[data-deferred-sortable-form]");
    if (!form) return;
    if (event.detail.successful) {
        finishDeferredSort(form);
        return;
    }

    const control = getModeControl(form);
    if (control) {
        control.disabled = false;
        if (form._sortableMode) control.value = form._sortableMode;
        setSortableMode(control);
    }
    setPendingActionsDisabled(form, false);
});
