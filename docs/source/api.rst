#########################################
 Application Programming Interface (API)
#########################################

.. toctree::
   :maxdepth: 2

   api/register
   api/describe
   api/collect
   api/evaluate

************
Excel Import
************

The Excel Import feature is designed to quickly populate a *Kora* database by importing data from an Excel workbook (XLSX). Excel Import is available through the browsable web API interface, which you can access from the user menu in the top navigation bar.

The Excel file columns must be named according to the fields expected by the importer. Please check the endpoint documentation for the accepted columns in the Excel table. The importer will always look for data in the first sheet of the provided spreadsheet. Please double-check that the relevant data is in the first sheet of the uploaded file.

At the moment, Excel Import functionality is available only for the following endpoints:

- `varieties` (:http:post:`/api/varieties/excel_import/`)
- `entities` (:http:post:`/api/entities/excel_import/`)
- `protections` (:http:post:`/api/protections/excel_import/`)

Access one of these endpoints in the browsable API, click the **"Extra Actions"** menu, and select **"Excel Import"**.

Importing Protection Data from Public Databases
===============================================

The Excel import endpoints can be used to import data from external sources such as the EU PVP (European Common Catalogue) or the CPVO website (Plant Breeder's Rights). These sources commonly provide data in Excel workbook format.

From one of the Excel import views, to import a new file:

1. Click the **Browse** button to select the file from your local machine.
2. Check the **Validate Only** box to check the file for errors without saving the data to the database.

Validation is performed upon upload, whether or not you choose to save the data. If validation errors are detected, the import is aborted and a row-by-row summary of errors, up to the first 100, is displayed.

.. warning::
   Remember to make a backup of the database before importing, in case you want to roll back.

Recommended Import Workflow
---------------------------

When importing protection data (`protections` endpoint, :http:post:`/api/protections/excel_import/`) from public databases, you will need to import the related reference records first. Public protection records often include variety denominations (`varieties` endpoint, :http:post:`/api/varieties/excel_import/`) and information about the owners of protection rights, such as applicants and maintainers (`entities` endpoint, :http:post:`/api/entities/excel_import/`). Because `protection` records refer to `varieties` and `entities` by string matching, those records must be imported before the protections themselves so that the references can be linked correctly. If you split the original data across multiple files for importing, make sure to preserve the strings exactly as they are, since the join depends on exact matching.

The import will attempt to relate varieties, applicants, and maintainers through string matching. If multiple matches exist in your database (e.g. two varieties of the same species with the same name), the importer cannot resolve the ambiguity; it will not associate the protection automatically and will return a validation error. In such cases, you need to remove the row from the file and either import manually through the user interface or use the API directly, where you can specify references using IDs.
