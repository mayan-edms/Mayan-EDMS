2.2 (2016-XX-XX)
================
- Remove the installation app (GitLab #301).
- Add support for document page search
- Remove recent searches feature
- Remove dependency on the django-filetransfer library
- Fix height calculation in resize transformation
- Improve upgrade instructions
- New image caching pipeline
- New drop down menus for the documents, folders and tags app as well as for
the user links
- New Dashboard view
- Moved licenses to their own module in every app
- Update project to work with Django 1.10.4.
- Tags are alphabetically ordered by label (GitLab #342).
- Stop loading theme fonts from the web (GitLab #343).
- Add support for attaching multiple tags (GitLab #307).


2.1.6 (2016-11-23)
=================
- Fix variable name typo in the rotation transformation class.
- Update translations

2.1.5 (2016-11-08)
==================
- Backport resize transformation math operation fix (GitLab #319).
- Update Pillow to 3.1.2 (Security fix).
- Backport zoom transformation performance improvement (GitLab #334).
- Backport trash can navigation link resolution fix (GitLab #331).
- Improve documentation regarding the use of GPG version 1 (GitLab #333).
- Fix ACL create view HTML response type. (GitLab #335).
- Expland staging folder and watch folder explanation.

2.1.4 (2016-10-28)
==================
- Add missing link to the 2.1.3 release notes in the index file.
- Improve TempfileCheckMixin.
- Fix statistics namespace list display view.
- Fix events list display view.
- Update required Django version to 1.8.15.
- Update required python-gnupg version to 0.3.9.
- Improved orphaned temporary files test mixin.
- Re-enable and improve GitLab CI MySQL testing.
- Improved GPG handling.
- New GPG backend system.
- Minor documentation updates.

2.1.3 (2016-06-29)
==================
- Add help message when initialsetup migration phase fails. Relates to GitLab issue #296.
- Start using self.setdout instead of print as per documentation.
- Fix GitLab issue #295, "When editing a user the top bar jumps to the name of the user".
- Normalize handling of temporary file and directory creation.
- Fix GitLab issue #309, "Temp files quickly filling-up my /tmp (1GB tmpfs)".
- Explicitly check for residual temporary files in tests.
- Add missing temporary file cleanup for office documents.
- Fix file descriptor leak in the document signature download test.

2.1.2 (2016-05-20)
==================
- Sort document languages and user profile locale language lists. GitLab issue #292.
- Fix metadata lookup for {{ users }} and {{ group }}. Fixes GitLab #290.
- Add Makefile for common development tasks

2.1.1 (2016-05-17)
==================
- Fix navigation issue that make it impossible to add new sources. GitLab issue #288.
- The Tesseract OCR backend now reports if the requested language file is missing. GitLab issue #289.
- Ensure the automatic default index is created after the default document type.

2.1 (2016-05-14)
================
- Upgrade to use Django 1.8.13. Issue #246.
- Upgrade requirements.
- Remove remaining references to Django's User model. GitLab issue #225
- Rename 'Content' search box to 'OCR'.
- Remove included login required middleware using django-stronghold instead (http://mikegrouchy.com/django-stronghold/).
- Improve generation of success and error messages for class based views.
- Remove ownership concept from folders.
- Replace strip_spaces middleware with the spaceless template tag. GitLab issue #255
- Deselect the update checkbox for optional metadata by default.
- Silence all Django 1.8 model import warnings.
- Implement per document type document creation permission. Closes GitLab issue #232.
- Add icons to the document face menu links.
- Increase icon to text spacing to 3px.
- Make document type delete time period optional.
- Fixed date locale handling in document properties, checkout and user detail views.
- Add new permission: checkout details view.
- Add HTML5 upload widget. Issue #162.
- Add Message of the Day app. Issue #222
- Update Document model's uuid field to use Django's native UUIDField class.
- Add new split view index navigation
- Newly uploaded documents appear in the Recent document list of the user.
- Document indexes now have ACL support.
- Remove the document index setup permission.
- Status messages now display the object class on which they operate not just the word "Object".
- More tests added.
- Handle unicode filenames in staging folders.
- Add staging file deletion permission.
- New document_signature_view permission.
- Add support for signing documents.
- Instead of multiple keyservers only one keyserver is now supported.
- Replace document type selection widget with an opened selection list.
- Add mailing documentation chapter.
- Add roadmap documentation chapter.
- API updates.


2.0.2 (2016-02-09)
==================
- Install testing dependencies when installing development dependencies.
- Fix GitLab issue #250 "Empty optional lookup metadata trigger validation error".
- Fix OCR API test.
- Move metadata form value validation to .clean() method.
- Only extract validation error messages from ValidationError exception instances.
- Don't store empty metadata value if the update checkbox is not checked.
- Add 2 second delay to document version tests to workaround MySQL limitation.
- Strip HTML tags from the browser title.
- Remove Docker and Docker Compose files.


2.0.1 (2016-01-22)
==================
- Fix GitLab issue #243, "System allows a user to skip entering values for a required metadata field while uploading a new document"
- Fix GitLab issue #245, "Add multiple metadata not possible"
- Updated Vagrantfile to provision a production box too.


2.0 (2015-12-04)
================
- New source homepage: https://gitlab.com/mayan-edms/mayan-edms
- Update to Django 1.7
- New Bootstrap Frontend UI
- Easier theming and rebranding
- Improved page navigation interface
- Menu reorganization
- Removal of famfam icon set
- Improved document preview generation
- Document submission for OCR changed to POST
- New YAML based settings system
- Removal of auto admin creation as separate app
- Removal of dependencies
- ACL system refactor
- Object access control inheritance
- Removal of anonymous user support
- Metadata validators refactor
- Trash can support
- Retention policies
- Support for sharing indexes as FUSE filesystems
- Clickable preview images titles
- Removal of eval
- Smarter OCR, per page parsing or OCR fallback
- Improve failure tolerance (not all Operational Errors are critical now)
- RGB tags
- Default document type and default document source
- Link unbinding
- Statistics refactor
- Apps merge
- New signals
- Test improvements
- Indexes recalculation after document creation too
- Upgrade command
- OCR data moved to ocr app from documents app
- New internal document creation workflow return a document stub
- Auto console debug logging during development and info during production
- New class based and menu based navigation system
- New class based transformations
- Usage of Font Awesome icons set
- Management command to remove obsolete permissions: `purgepermissions`
- Normalization of 'title' and 'name' fields to 'label'
- Improved API, now at version 1
- Invert page title/project name order in browser title
- Django's class based views pagination
- Reduction of text strings
- Removal of the CombinedSource class
- Removal of default class ACLs
- Removal of the ImageMagick and GraphicsMagick converter backends
- Remove support for applying roles to new users automatically
- Removal of the DOCUMENT_RESTRICTIONS_OVERRIDE permission
- Removed the page_label field


1.1.1 (2015-05-21)
==================

- Update to Django 1.6.11
- Fix make_dist.sh script
- Add test for issue #163
- Activate tests for the sources app
- Removal of the registration app
- New simplified official project description
- Improvements to the index admin interface
- Removal of installation statistics gathering
- Remove unused folder tag
- Fix usage of ugettext to ugettext_lazy
- Increase size of the lock name field
- New style documentation


1.1 (2015-02-10)
================
- Uses Celery for background tasks
- Removal of the splash screen
- Adds a home view with common function buttons
- Support for sending and receiving documents via email
- Removed custom logging app in favor of django-actvity-stream
- Adds watch folders
- Includes Vagrant file for unified development and testing environments
- Per user locale profile (language and timezone)
- Includes news document workflow app
- Optional and required metadata types
- Improved testings. Automated tests against SQLite, MySQL, PostgreSQL
- Many new REST API endpoints added
- Simplified text messages
- Improved method for custom settings
- Addition of CORS support to the REST API
- Per document language setting instead of per installation language setting
- Metadata validation and parsing support
- Start of code updates towards Python 3 support
- Simplified UI
- Stable PDF previews generation
- More technical documentation


1.0 (2014-08-27)
================
- New home @ https://github.com/mayan-edms/mayan-edms
- Updated to use Django 1.6
- Translation updates
- Custom model properties removal
- Source code improvements
- Removal of included 3rd party modules
- Automatic testing and code coverage check
- Update of required modules and libraries versions
- Database connection leaks fixes
- Support for deletion of detached signatures
- Removal of Fabric based installations script
- Pluggable OCR backends
- OCR improvements
- License change, Mayan EDMS in now licensed under the Apache 2.0 License
- PyPI package, Mayan EDMS in now available on PyPI: https://pypi.python.org/pypi/mayan-edms/
- New REST API
