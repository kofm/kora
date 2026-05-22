/* =========
 * TomSelect
 * ========= */

function renderLabelOption(data, escape) {
    const value = escape(data.value);
    const colour = data.colour || `label-${value}`;
    const text = escape(data.text);

    return `
            <div class="d-flex align-items-center ts-colour">
                <span class="badge rounded-pill ${colour}">
                    ${text}
                </span>
            </div>
        `;
}

function bindDependentTomSelect(el) {
    const dependsOn = el.dataset.tsDependsOn;
    if (!dependsOn) return;

    const parent = document.getElementById(`id_${dependsOn}`);
    if (!parent) return;

    const child = el.tomselect;
    if (!child) return;

    // Select should be disabled if there is no parent value
    const setChildStatus = () => {
        const parentValue = parent.tomselect?.getValue() || parent.value;
        if (parentValue) {
            child.enable();
            child.load("");
        } else {
            child.disable();
        }
    };

    const clearChild = () => {
        child.clear();
        child.clearOptions();
        child.disable();
        setChildStatus();
    };

    if (parent.tomselect) {
        parent.tomselect.on("change", clearChild);
        // When DOM is swapped via HTMX we use the to kill the event listener
        el._tomselectCleanup = () => {
            parent.tomselect?.off("change", clearChild);
        };
    } else {
        parent.addEventListener("change", clearChild);
    }

    // Initial status of the input
    setChildStatus();
}

function parseDataValue(value) {
    if (value === "true") return true;
    if (value === "false") return false;

    if (!Number.isNaN(Number(value)) && value.trim() !== "") {
        return Number(value);
    }

    const trimmed = value.trim();

    if (
        (trimmed.startsWith("[") && trimmed.endsWith("]")) ||
        (trimmed.startsWith("{") && trimmed.endsWith("}"))
    ) {
        try {
            return JSON.parse(trimmed);
        } catch {
            return value;
        }
    }

    return value;
}

function asOptions(el) {
    const opts = {};

    for (const attr of el.attributes) {
        if (!attr.name.startsWith("data-ts-")) continue;

        const key = attr.name
            .replace("data-ts-", "")
            .replace(/-([a-z])/g, (_, c) => c.toUpperCase());

        opts[key] = parseDataValue(attr.value);
    }

    if (opts.url) {
        const url = opts.url;
        const searchParam = opts.searchParam;
        const dependsOn = opts.dependsOn;
        const dependsParam = opts.dependsParam;

        delete opts.url;
        delete opts.dependsOn;
        delete opts.dependsParam;
        opts.load = async function (query, callback) {
            const params = new URLSearchParams();
            params.set("q", query);
            if (dependsOn) {
                if (!dependsParam) throw new Error("`dependsParam` must be defined");
                const parent = document.getElementById(`id_${dependsOn}`);
                const parentValue = parent?.tomselect?.getValue() || parent?.value;

                if (!parentValue) {
                    callback([]);
                    return;
                }

                params.set(dependsParam, parentValue);
            }

            try {
                const response = await fetch(`${url}?${params}`);
                if (!response.ok) throw new Error("TomSelect fetch failed");

                const data = await response.json();
                callback(data.results);
            } catch {
                callback([]);
            }
        };
    }

    if (opts.colour) {
        delete opts.colour;

        opts.render = {
            option: renderLabelOption,
            item: renderLabelOption,
            ...(opts.render || {}),
        };
    }

    return opts;
}

export function initializeTomSelects(root = document) {
    if (!window.TomSelect) return;
    root.querySelectorAll("select.tomselect").forEach((el) => {
        const opts = asOptions(el);
        if (el.tomselect) return;
        new window.TomSelect(el, opts);
        bindDependentTomSelect(el);
    });
}
