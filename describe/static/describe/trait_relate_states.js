new TomSelect("#id_protocol", {
    valueField: "id",
    labelField: "name",
    searchField: "name",
    preload: true,
    placeholder: "Select a Protocol...",
    load: function (_query, callback) {
        if (this.loading > 1) {
            callback();
            return;
        }

        const protocolsListUrl = JSON.parse(
            document.getElementById("protocols-list-url").textContent,
        );

        fetch(protocolsListUrl)
            .then((response) => response.json())
            .then((json) => {
                callback(json);
                this.settings.load = null;
            })
            .catch(() => callback());
    },
    onChange: function (value) {
        const traitSearchUrl = JSON.parse(
            document.getElementById("trait-search-url").textContent,
        );
        if (value) {
            fetch(`${traitSearchUrl}?no_pagination=1&protocol=${value}`)
                .then((response) => response.json())
                .then((json) => {
                    control.clear();
                    control.clearOptions();
                    control.addOptions(json);
                    control.refreshOptions(false);
                    control.enable();
                });
        } else {
            control.clear();
            control.clearOptions();
            control.disable();
        }
    },
});

const mapButton = document.getElementById("map-button");
const resetButton = document.getElementById("reset-button");

function updateButtons() {
    const value = control.getValue();
    const emptyTrait = document.querySelector("#targets > .empty-state");
    const canReset = !emptyTrait;
    const canMap = value && !emptyTrait;

    mapButton.classList.toggle("disabled", !canMap);
    resetButton.classList.toggle("disabled", !canReset);
}

const control = new TomSelect("#id_trait", {
    valueField: "id",
    labelField: "description",
    searchField: "description",
    openOnFocus: true,
    placeholder: "Select a Trait...",
    maxOptions: 100,
    onInitialize: function () {
        this.disable();
    },
    onChange: function (value) {
        htmx.trigger("#available-states", "trait-selected");
    },
    render: {
        option: function (data, escape) {
            return `<div>${escape(data.numeric_id)}. ${escape(data.description)}</div>`;
        },
        item: function (data, escape) {
            return `<div>${escape(data.numeric_id)}. ${escape(data.description)}</div>`;
        },
    },
});

function getStateIds(list) {
    return [...list.querySelectorAll(":scope > .state-item")]
        .map((item) => item.dataset.id);
}

new window.Sortable(document.getElementById("available-states"), {
    group: {
        name: "relations",
        pull: "clone",
        put: false,
    },
    sort: false,
    animation: 150,
});

function initTargetSortables(root = document) {
    // htmx can replace target lists with fresh DOM nodes.
    // Re-initialize Sortable on new `.target-items`, avoiding duplicates.
    root.querySelectorAll(".target-items").forEach((list) => {
        if (list.dataset.sortableInitialized === "true") {
            return;
        }

        new Sortable(list, {
            group: {
                name: "relations",
                pull: true,
                put: true,
            },
            filter: ".bg-body-tertiary, .bg-info-subtle",
            sort: false,
            animation: 150,

            onAdd(event) {
                const targetState = event.to;
                const sourceState = event.clone;
                const url = sourceState.dataset.updateUrl;

                console.log(url);

                htmx.ajax("POST", url, {
                    "swap": "none",
                    "values": {
                        target_state_id: targetState.dataset.id,
                    },
                });
            },
        });

        list.dataset.sortableInitialized = "true";
    });
}

initTargetSortables();
document.body.addEventListener("htmx:afterSwap", (event) => {
    initTargetSortables(event.detail.elt);
    updateButtons();
});
