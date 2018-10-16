***
API
***

Mayan EDMS provides an HTTP REST Application Program Interface (or API). This
API allows integration with 3rd party software using simple HTTP requests.

Several API authentication methods are provides: **Session**, **Token**,
and **HTTP Basic**.

The URL for the API can be found via the :menuselection:`Tools --> REST API
menu. The API is also self-documenting. The live API documentation can be
found in the :menuselection:`Tools --> API Documentation (Swagger)` menu for
the Swagger version and in the
:menuselection:`Tools --> API Documentation (ReDoc)` menu for the ReDoc version.

The are a few ways to structure REST APIs. In the case of Mayan EDMS, API
endpoints are structured by resource type. Examples:

* /cabinets - To view or create new cabinets
* /cabinets/<id> - To view the details, edit, or delete an existing cabinet.
* /cabinets/<id>/documents - To view, add, or remove documents from an existing
  cabinet.
* /cabinets/<id>/documents/<id> - To view, add, or remove one document from an
  existing cabinet.

The API supports the HTTP verbs: **GET**, **POST**, **PUT**, **PATCH**,
and **DELETE**.
