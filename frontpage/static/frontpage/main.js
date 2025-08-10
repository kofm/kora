// frontpage/static/frontpage/main.js
// Assumes vendor globals already loaded: bootstrap, htmx, TomSelect, Sortable
(() => {
  'use strict';

  /* ===========================
   * Bootstrap helpers
   * =========================== */
  function initializeTooltips(root = document) {
    if (!window.bootstrap) return;
    root.querySelectorAll('[data-bs-toggle="tooltip"]').forEach((el) => {
      new window.bootstrap.Tooltip(el);
    });
  }

  function closeModalById(modalId = 'modal') {
    if (!window.bootstrap) return;
    const el = document.getElementById(modalId);
    if (!el) return;
    let modal = window.bootstrap.Modal.getInstance(el);
    if (!modal) modal = new window.bootstrap.Modal(el);
    modal.hide();
  }

  function initializeToast(element) {
    if (!window.bootstrap) return;
    let toast = window.bootstrap.Toast.getInstance(element);
    if (!toast) {
      toast = new window.bootstrap.Toast(element);
      toast.show();
    } else if (!toast.isShown()) {
      toast.dispose();
      element.remove();
    }
  }

  /* ===========================
   * TomSelect helpers + htmx extension
   * =========================== */
  function asOptions(el) {
    const opts = {};
    for (const attr of el.attributes) {
      if (!attr.name.startsWith('data-ts-')) continue;
      const k = attr.name
        .replace('data-ts-', '')
        .replace(/-([a-z])/g, (_, c) => c.toUpperCase());
      let v = attr.value;
      if (v === 'true') v = true;
      else if (v === 'false') v = false;
      else if (!isNaN(v) && v.trim() !== '') v = Number(v);
      opts[k] = v;
    }
    return opts;
  }

  function initializeTomSelects(root = document) {
    if (!window.TomSelect) return;
    root.querySelectorAll('select.tomselect').forEach((el) => {
      if (!el.tomselect) el.tomselect = new window.TomSelect(el, asOptions(el));
    });
  }

  function registerTomSelectExtension(htmx) {
    if (!htmx || !window.TomSelect) return;
    htmx.defineExtension('tomselect', {
      onEvent: function (name, evt) {
        if (name === 'htmx:beforeSwap') {
          const elt = evt.detail.target;
          if (elt) {
            elt.querySelectorAll('select.tomselect').forEach((el) => {
              if (el.tomselect) el.tomselect.destroy();
            });
          }
        }
        if (name === 'htmx:afterSettle') {
          const elt = evt.detail.elt;
          if (elt) {
            elt.querySelectorAll('select.tomselect').forEach((el) => {
              if (!el.tomselect) el.tomselect = new window.TomSelect(el, asOptions(el));
            });
          }
        }
      },
    });
  }

  /* ===========================
   * Sortable
   * =========================== */
  function initializeSortableElements(container = document) {
    if (!window.Sortable) return;
    container.querySelectorAll('.sortable').forEach((element) => {
      if (element._sortable) element._sortable.destroy();
      element._sortable = new window.Sortable(element, {
        animation: 150,
        sort: element.dataset.sortable === 'true',
      });
    });
  }

  /* ===========================
   * Boot
   * =========================== */
  document.addEventListener('DOMContentLoaded', () => {
    initializeTooltips();
    initializeTomSelects();
    initializeSortableElements(document);

    document.body.addEventListener('closeModal', () => closeModalById('modal'));
  });

  if (window.htmx) {
    registerTomSelectExtension(window.htmx);

    document.addEventListener('htmx:afterSwap', () => {
      initializeSortableElements(document);
    });

    window.htmx.onLoad(() => {
      window.htmx.findAll('.toast').forEach((el) => initializeToast(el));
    });
  }
})();
