(() => {
    const root = document.documentElement;
    const systemTheme = typeof window.matchMedia === "function"
        ? window.matchMedia("(prefers-color-scheme: dark)")
        : null;

    function applyTheme() {
        const preference = root.dataset.appearance;
        root.dataset.bsTheme = preference === "auto"
            ? (systemTheme?.matches ? "dark" : "light")
            : preference;
    }

    function updateMenu() {
        document.querySelectorAll("[data-appearance-choice]").forEach((button) => {
            const selected = button.dataset.appearanceChoice === root.dataset.appearance;
            button.classList.toggle("active", selected);
            button.setAttribute("aria-pressed", String(selected));
        });
    }

    applyTheme();
    systemTheme?.addEventListener("change", () => {
        if (root.dataset.appearance === "auto") applyTheme();
    });

    document.addEventListener("click", (event) => {
        const button = event.target.closest("[data-appearance-choice]");
        if (!button) return;
        root.dataset.appearance = button.dataset.appearanceChoice;
        applyTheme();
        updateMenu();
    });
})();
