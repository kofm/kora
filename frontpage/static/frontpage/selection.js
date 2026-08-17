function selectionInput(gridItem) {
    return gridItem.querySelector('input[name="selection"]');
}

function setSelected(gridItem, selected) {
    const input = selectionInput(gridItem);
    if (selected === Boolean(input)) return;

    if (input) {
        input.remove();
        return;
    }

    const value = gridItem.querySelector('input[name="order"]')?.value;
    if (!value) return;

    const newInput = document.createElement("input");
    newInput.type = "hidden";
    newInput.name = "selection";
    newInput.value = value;
    gridItem.append(newInput);
}

function updateSelectionControls(grid) {
    const selectedItems = grid.querySelectorAll('.grid-item input[name="selection"]');
    const selectionCount = selectedItems.length;

    grid.querySelectorAll(".grid-item").forEach((gridItem) => {
        gridItem.classList.toggle("border-primary", Boolean(selectionInput(gridItem)));
    });

    document.querySelectorAll("[data-selection-status]").forEach((status) => {
        status.textContent = selectionCount === 1 ? "1 crop selected" : `${selectionCount} crops selected`;
    });

    document.querySelectorAll("[data-requires-selection]").forEach((control) => {
        control.disabled = selectionCount === 0;
    });
}

function selectedValues(grid) {
    return Array.from(grid.querySelectorAll('.grid-item input[name="selection"]'), (input) => input.value);
}

function selectableGrid(container) {
    return container.matches?.("[data-selectable-grid]")
        ? container
        : container.querySelector?.("[data-selectable-grid]");
}

function restoreSelection(grid, values) {
    const selected = new Set(values);
    grid.querySelectorAll(".grid-item").forEach((gridItem) => {
        const value = gridItem.querySelector('input[name="order"]')?.value;
        setSelected(gridItem, selected.has(value));
    });
    updateSelectionControls(grid);
}

let preservedSelection = [];

document.addEventListener("click", (event) => {
    const action = event.target.closest("[data-selection-action]");
    const grid = document.querySelector("[data-selectable-grid]");
    if (!grid) return;

    if (action) {
        const selected = action.dataset.selectionAction === "all";
        grid.querySelectorAll(".grid-item").forEach((gridItem) => setSelected(gridItem, selected));
        updateSelectionControls(grid);
        return;
    }

    const gridItem = event.target.closest("[data-selectable-grid] .grid-item");
    if (!gridItem || event.target.closest("a, button, input, select, textarea")) return;

    setSelected(gridItem, !selectionInput(gridItem));
    updateSelectionControls(grid);
});

document.body.addEventListener("htmx:beforeSwap", (event) => {
    const grid = selectableGrid(event.detail.target);
    if (grid) preservedSelection = selectedValues(grid);
});

document.body.addEventListener("htmx:afterSwap", (event) => {
    const grid = selectableGrid(event.detail.target);
    if (grid) restoreSelection(grid, preservedSelection);
});

document.addEventListener("DOMContentLoaded", () => {
    const grid = document.querySelector("[data-selectable-grid]");
    if (grid) updateSelectionControls(grid);
});
