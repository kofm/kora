## 0.5.2 (2025-06-13)

### Added

- **register**: add species filter in Protection listing
- **restapi**: enhance Excel import with better error handling and performance

### Fixed

- **register**: correct queryset filtering in ProtectionOmniFilter

## 0.5.1 (2025-06-12)

### Fixed

- **restapi**: improve excel import validation and error handling

## 0.5.0 (2025-06-11)

### Added

- **frontpage**: add API link to user menu for superusers
- **restapi**: add Excel import endpoints and serializers for PlantVariety, Entity, and Protection
- **restapi**: support bulk create in main viewsets and serializers

### Fixed

- **register**: restore Protection table functionality in Variety detail page
- **describe**: make protocol queryset dynamic in RelatedStateForm

## 0.4.1 (2025-05-21)

### Fixed

- **describe**: resolved missing varieties bug in Description creation

## 0.4.0 (2025-05-21)

### Added

- **restapi**: add new API endpoint for States of Expressions
- **frontpage**: new homepage layout
- **frontpage**: Django Admin interface is now accessible from the Admin page
- **spaces**: add permission checks and signals for user groups and model permissions
- **spaces**: refactor area duplication and reorder URL patterns
- add django-easy-audit integration
- **spaces**: rename URL patterns to use snake_case
- **spaces**: enhance location detail view with area grid and update models
- **django_sortable_htmx**: add sortable grid and update card div templates
- **collect,frontpage,register**: add model factories and provide some testing
- **restapi**: add Cart model API endpoints and serializer
- **spaces**: refactor spaces app with HTMX support, improve UI, breadcrumbs, and permissions
- **register**: enhance entity list with filters, HTMX, and pagination consistency
- **user**: introduce authentication, permission system, and UI enhancements

### Fixed

- **protocol**: refine protocol update view and templates UI
- **collect**: enhance sample filtering and UI, rename form in register filters
- **describe**: refactor and improve expression forms and views
- **frontpage**: make logger dedicated to failed login attempts
- **describe**: remove unused import templates
- cleanup and typing improvements across multiple apps
- **breadcrumbs**: skip breadcrumb generation for HTMX requests and handle empty breadcrumbs
- **collect**: improve sample weight display and retrieval

### Documentation

- **frontpage**: add installation and security documentation; enhance configuration docs
- add Sphinx documentation setup and initial docs content

## 0.3.1 (2025-04-30)

### Feat

- **restapi**: add date fields to ProtectionSerializer
- **collect**: enhance form submission UX in partials
- **describe**: improve description list UI and workspace element create with messages
- **collect**: add sample weight reservation system and improve cart UI and validation
- **collect**: prevent deletion of Samples which are held in a Cart
- **frontpage**: add HTMX toast notifications and improve message handling
- **describe**: improve workspace detail and offcanvas layout
- add GitHub Actions to automate submodule update in kora-docker

### Fix

- **collect**: refactor storage counts, forms, and views; remove deprecated code
- **describe**: initialize session before updating description_filter
- **collect, describe**: restrict add-to-cart and add-to-workspace buttons to authenticated users
- **collect**: improve cart detail and offcanvas layout

### Refactor

- **frontpage**: replace div.container with main.container in base.html

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
