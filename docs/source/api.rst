#####
 API
#####

************
Excel Import
************

The Excel Import feature is designed to help non-technical users to
quickly populate their *kora* database by importing data from in Excel
Workbook format (xlsx).

Accessing Excel Import
======================

You can access the Excel Import functionality through the browsable
web API interface. 

- Log into *kora* with an account that has the necessary permissions.
- Use the user menu to navigate to the API.
- The API main page displays all the available digital locations where
  the API can provide or receive data; these are called **endpoints**.
- At the moment, Excel Import functionality is available only for a
  selected number of endpoints, i.e.:

  - **varieties**
  
  - **entities**
  
  - **protections**

- From each endpoint, you can click the **"extra actions"** menu and
  select **"excel import"**.

This will open the Excel Import page for that type of data.

Importing Protection Data
=========================

The Excel Import endpoints provide an efficient way to populate your
*kora* instance with plant genetic resource data by leveraging public
datasets.  With this functionality it's easy to import data from
external sources like the EU PVP (European Common Catalogue) or the
CPVO website (Plant Breeder's Rights). These sources commonly provide
data in Excel Workbook format.

On the Excel Import page you will find:

- A **Browse** button to select the Excel file from your local
  machine.
- A **Validate Only** checkbox to run validation without saving data
  to the database.

.. note::
    Validation is always performed upon upload, whether or not you
    choose to save the data.

If validation errors are detected:

- The import is aborted.
- A row-by-row summary of errors is displayed (truncated at the first
  100 errors for performance reasons).

.. warning::
   Always make a backup of your database before importing, so you can
   roll back should you encounter undesired effects.

Recommended Import Workflow
---------------------------

To maintain data integrity, perform imports in this sequence:

1. **Varieties**

2. **Entities** (applicants and maintainers)

3. **Protections**

This order ensures relational data can be correctly linked.

Guidelines for Excel Files
--------------------------

- **Naming Columns**

  The Excel file columns must be named according to the fields
  expected by the importer:

  - *Varieties*

    - `name`: Name of the variety (required).
  
    - `species`: The primary key (ID) of the species (required).

  - *Entities*

    - `name`: Name of the entity (required).
  
    - `type`: Type of entity (optional). Must match one of the allowed values.
  
    - `country`: Country code (optional).
  
    - `contact`: Contact information (optional).
  
    - `email`: Email address (optional).

  - *Protections*

    - `name`: Name of the variety (required).
  
    - `species_id`: The primary key (ID) of the species (required).
  
    - `type`: Protection type (required, see choices below).
  
    - `reference`: Reference string (optional).
  
    - `status`: Protection status (optional).
  
    - `country`: Country code (optional).
  
    - `date_start`: Start date of protection (optional).
  
    - `date_end`: End date of protection (optional).
  
    - `applicants`: Semi-colon separated list of applicant names (optional).
  
    - `maintainers`: Semi-colon separated list of maintainer names (optional).
  
    - `note`: Additional notes (optional).

.. note::
   The importer will always look for data **in the first sheet of the
   provided spreadsheet**. Please double check that the relevant data
   is in the first sheet of the uploaded file.

- **Species IDs for Varieties**

  To find the correct `species` IDs for variety and protection import:

  - Navigate to the *species* endpoint in the browsable API.
  - Retrieve the list of species and take note of their primary keys (IDs).
  - Use these IDs in the `species` column of your varieties Excel file.

- **Handling Duplicates**

  - *Varieties:* If a variety with the same name for the same species already exists, it will **not** be imported again to avoid duplicates.

  - *Entities:* When importing entities, each entity name must be on its own row.
  
    - Avoid using semi-colon separated names in the entities import file, as these will be imported as a single entity.
    
    - To split multiple entity names into separate rows, you can use Excel formulas or text-to-columns tools before importing.

- **Multiple Applicants and Maintainers in Protections**

  - The `applicants` and `maintainers` columns in the protection import file accept multiple entities.
  
  - These should be entered as semi-colon separated names (e.g. `"Entity A; Entity B"`). This format is commonly used by public databases.

- **Entity and Variety Matching for Protections**

  - The import will attempt to relate applicants, maintainers, and varieties through string matching.
  
  - If two variety with the same name and species exists in your
    database, the importer cannot resolve this ambiguity and it will
    **not** associate the protection automatically, resulting in a
    validation error. In such cases, you need to remove the row from
    the file and either:
  
    - Import manually via the user interface or
    
    - Use the API directly referencing primary keys.

Valid Choices for Select Fields
-------------------------------

When preparing your Excel files, ensure the values for choice fields are encoded correctly. Use these mappings for replacement or find-and-replace operations:

- **Entity Types** (for entities `type` field):

  - `IN` — Individual
  
  - `PA` — Partnership
  
  - `CO` — Company
  
  - `CP` — Cooperative

- **Protection Types** (for protections `type` field):

  - `PBR` — Plant Breeders' Rights
  
  - `NLI` — National Listing
  
  - `CAT` — Common Catalogue

- **Protection Statuses** (for protections `status` field):

  - `G` — Granted
  
  - `T` — Terminated
  
  - `A` — Active Application
  
  - `W` — Withdrawn
  
  - `R` — Refused
  
  - `S` — Surrendered

Examples:
  
- Replace values like `"Granted"` with `"G"`.
  
- Replace `"Individual"` with `"IN"` in entity type.

Summary
-------

Remember:

- Backup your database before importing.

- Use the browsable API "extra actions" menus to access the import pages.

- Perform import in the order: varieties → entities → protections.

- For complex relations or duplicates, consider manual or data entry
  via the API.
