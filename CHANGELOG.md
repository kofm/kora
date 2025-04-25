## 0.3.0 (2025-04-25)

### Feat

- **frontpage**: update detail and list page headers design for clarity and emphasis
- **collect**: enhance sample and germinability management
- add django-browser-reload for development convenience
- enable timezone support
- enhance frontpage and register modules
- **frontpage**: add TomSelect widgets and remove obsolete assets
- enhance form and library initialization
- **describe**: support htmx partial updates and streamline rendering
- **collect**: comprehensive update for sample management
- add htmx block rendering decorator

### Fix

- **collect**: resolve cart item display and retrieval issues
- replace manual HX-Request header checks with is_htmx utility
- **middleware**: handle HTMX redirects to login with referer
- date input formats updated
- **breadcrumbs**: update type handling in breadcrumbs utils
- **collect**: sample weight is now showing correctly in sample_detail view

### Refactor

- **frontpage**: update login template to extend base layout
- **frontpage**: remove time from card_col_rows and update sample_detail view accordingly
- optimize form handling and modularize assets
- **describe**: simplify form handling in description views
- **collect**: rename 'SeedSample' model to 'Sample'
- **collect**: update URL paths and template references for sample management
- enhance dropdown handling and modal interfaces

## 0.2.0 (2025-04-14)

### Feat

- **modal**: implement modal-based cart management with HTMX
- **cart**: add "empty cart" functionality

### Fix

- **describe**: address situations where a protocol is not yet defined

### Refactor

- **collect**: rename 'Accessions' to 'Samples'

### Perf

- **cart**: optimize cart item retrieval with select_related
