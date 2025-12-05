## 0.5.13 (2025-12-05)

### Fixed

- **collect**: restore the storage deletion functionality

## 0.5.12 (2025-12-04)

### Fixed

- **register**: improve variety search by displaying results ranked by similarity (exact matches at the top)
- **register**: email is not anymore required when creating a new Entity
- **register**: fix inconsistent naming of Protection reference
- **register**: fix country display in Protection detail view
- **collect**: restore notes field to Sample form
- **frontpage**: restore css for table interaction
- **register**: remove obsolete protection update template and simplify view rendering

## 0.5.11 (2025-08-28)

### Fixed

- **restapi**: include 'note' field in ProtectionSerializer

## 0.5.10 (2025-08-05)

### Added

- **frontpage**: update Bootstrap Icons to v1.13.1 and add new icon fonts

### Fixed

- **describe**: add unique constraint on Trait numeric_id per protocol

### Documentation

- add detailed API documentation for Excel Import feature

## 0.5.9 (2025-06-27)

### Fixed

- **register**: redirect to entity list after deletion instead of detail view

## 0.5.8 (2025-06-27)

### Fixed

- **register**: simplify PlantVarietyEntityTable by removing country column
- **register**: correct success_url in ProtectionDeleteView and EntityDeleteView

## 0.5.7 (2025-06-27)

### Fixed

- **register**: correctly display related plant varieties on entity detail page
- **register**: set correct success URL after protection deletion

## 0.5.6 (2025-06-27)

### Added

- **register**: add entity filtering to ProtectionOmniFilter

### Fixed

- **register**: add missing permission requirement for ProtectionDeleteView
- **describe**: improve error display on Trait form

## 0.5.5 (2025-06-24)

### Fixed

- pin Django to 5.2 and downgrade sqlparse to 0.5.3 for compatibility

## 0.5.4 (2025-06-24)

### Fixed

- **describe**: enforce unique Trait numeric ID per protocol and improve Trait form UI
- **frontpage**: make clear button URL default empty to avoid reload issues

## 0.5.3 (2025-06-16)

### Added

- **register**: enhance plant species and variety lists cards UI
- **register**: add searchable Plant Species list with card view and pagination
- **register**: improve search UI and layout consistency across listing pages
- **describe**: improve UI and export link formatting in description list
- **register**: improve Plant Variety search, filter, and listing UI

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
