function synchronizeColumnIndices(wrapper) {
    const scrollContainer = wrapper.querySelector(".grid-layout-scroll");
    const grid = scrollContainer?.querySelector(".grid-layout");
    const columnIndices = wrapper.querySelector(".grid-layout-column-indices");
    if (!scrollContainer || !grid || !columnIndices) return;

    const updateWidth = () => {
        columnIndices.style.width = `${grid.scrollWidth}px`;
    };
    const updatePosition = () => {
        columnIndices.style.transform = `translateX(-${scrollContainer.scrollLeft}px)`;
    };

    scrollContainer.addEventListener("scroll", updatePosition, { passive: true });
    const resizeObserver = new ResizeObserver(updateWidth);
    resizeObserver.observe(grid);

    updateWidth();
    updatePosition();
    wrapper._coordinateCleanup = () => {
        scrollContainer.removeEventListener("scroll", updatePosition);
        resizeObserver.disconnect();
    };
}

export function initializeCoordinateGrids(container = document) {
    container.querySelectorAll(".grid-layout-coordinate-wrapper").forEach((wrapper) => {
        wrapper._coordinateCleanup?.();
        synchronizeColumnIndices(wrapper);
    });
}
