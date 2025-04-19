import TomSelect from "tom-select";

function asOptions(el) {
    const opts = {};
    for (const attr of el.attributes) {
        if (attr.name.startsWith("data-ts-")) {
            const k = attr.name
                .replace("data-ts-", "")
                .replace(/-([a-z])/g, (_, c) => c.toUpperCase());
            let v = attr.value;
            if (v === "true") v = true;
            else if (v === "false") v = false;
            else if (!isNaN(v) && v.trim() !== "") v = Number(v);
            opts[k] = v;
        }
    }
    return opts;
}

export function initializeTomSelects(root = document) {
    root.querySelectorAll('select.tomselect').forEach((el) => {
        if (!el.tomselect) {
            el.tomselect = new TomSelect(el, asOptions(el));
        }
    });
}

export function registerTomSelectExtension(htmx) {
    htmx.defineExtension('tomselect', {
        onEvent: function(name, evt) {
            if (name === 'htmx:beforeSwap') {
                const elt = evt.detail.target;
                if (elt) {
                    elt.querySelectorAll('select.tomselect').forEach((el) => {
                        if (el.tomselect) {
                            el.tomselect.destroy();
                        }
                    });
                }
            }
            if (name === 'htmx:afterSettle') {
                const elt = evt.detail.elt;
                if (elt) {
                    elt.querySelectorAll('select.tomselect').forEach((el) => {
                        if (!el.tomselect) {
                            el.tomselect = new TomSelect(el, asOptions(el));
                        }
                    });
                }
            }
        }
    });
}
