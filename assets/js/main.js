import "../scss/bootstrap.scss";
import * as Popper from "@popperjs/core";
import TomSelect from "tom-select";
import htmx from "htmx.org";
// The following is necessary to load Hyperscript. See https://github.com/bigskysoftware/_hyperscript/issues/162
window._hyperscript = require('hyperscript.org');
window._hyperscript.browserInit();

import { initializeTomSelects, registerTomSelectExtension } from "./widgets/tomselect.js";
import { initializeTooltips, closeModalById, initializeToast } from "./bootstrap-init.js";

window.TomSelect = TomSelect;
window.htmx = htmx;

registerTomSelectExtension(htmx);

document.addEventListener("DOMContentLoaded", function () {
    initializeTooltips();
    initializeTomSelects();

    document.body.addEventListener('closeModal', function() {
        closeModalById("modal");
    });

    htmx.onLoad(() => {
	htmx.findAll(".toast").forEach((element) => {
	    initializeToast(element);
	})
    })
});
