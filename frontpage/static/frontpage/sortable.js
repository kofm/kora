/* =========
 * Sortable
 * ========= */
export function initializeSortableElements(container = document) {
    if (!window.Sortable) return;
    container.querySelectorAll(".sortable").forEach((element) => {
        if (element._sortable) element._sortable.destroy();
        element._sortable = new window.Sortable(element, {
            animation: 150,
            sort: element.dataset.sortable === "true",
        });
    });
}
