- Use Select2 widget for the document type selection form.
- Update source column matching to be additive and not exclusive.
- Add two columns to show the number of documents per workflow and
  workflow state.
- Sort module.
- Add link to sort individual indexes.
- Support exclusions from source columns.
- Improve source column exclusion. Improve for model subclasses in partial querysets.
- Add sortable index instance label column.
- Add rectangle drawing transformation.
- Redactions app.
- Remove duplicated trashed document preview.
- Add label to trashed date and time document source column.
- Tag created event fix.

3.2.3 (2019-06-21)
* Add a reusable task to upload documents.
* Add MVP of the importer app.

3.2.4-3.2.8 (2019-10-07)

Merge with 3.3.6 (2019-12-20)
- Removed local file caching 0003_auto_20191008_1510.py.
  This migration is equal to upstream 0003 migrations. Solution is to delete
  upstream migration.
- Conflict with upstream migrations 0052_auto_20191130_2209.py.
  This migration add the related name "version_pages" to DocumentPage which is
  not necesarry as this branch has a different model structure.
  Solution is to delete upstream migration.

