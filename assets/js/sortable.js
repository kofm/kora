// Sortable.js
import "../css/sortable.css";
import Sortable from 'sortablejs';
window.Sortable = Sortable;

document.addEventListener("DOMContentLoaded", function() {
    initializeSortableElements(document);
});

document.addEventListener("htmx:afterSwap", function() {
    initializeSortableElements(document);
});

function initializeSortableElements(container) {
    const sortableElements = container.querySelectorAll('.sortable');

    sortableElements.forEach(element => {
	if (element._sortable) {
	    element._sortable.destroy();
	}

	element._sortable = new Sortable(element, {
	    animation: 150,
	    sort: element.dataset.sortable === 'true'
	});
    });
}
