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


Example use
===========

Install Python Requests (http://docs.python-requests.org/en/master/)::

    pip install requests

Get a list of document types::

    import requests

    requests.get('http://127.0.0.1:8000/api/document_types/', auth=('username', 'password')).json()

    {u'count': 1,
     u'next': None,
     u'previous': None,
     u'results': [{u'delete_time_period': 30,
       u'delete_time_unit': u'days',
       u'documents_count': 12,
       u'documents_url': u'http://127.0.0.1:8000/api/document_types/1/documents/',
       u'filenames': [],
       u'id': 1,
       u'label': u'Default',
       u'trash_time_period': None,
       u'trash_time_unit': None,
       u'url': u'http://127.0.0.1:8000/api/document_types/1/'}]}

Upload a new document::

    with open('test_document.pdf', mode='rb') as
        requests.post('http://127.0.0.1:8000/api/documents/', auth=('username', 'password'), files={'file': file_object}, data={'document_type': 1}).json()

    {u'description': u'',
    u'document_type': 1,
    u'id': 19,
    u'label': u'test_document.pdf',
    u'language': u'eng'}

Use API tokens to avoid sending the username and password on every request. Obtain a token by making a POST request to ``/api/auth/token/obtain/?format=json``::

    requests.post('http://127.0.0.1:8000/api/auth/token/obtain/?format=json', data={'username': 'username', 'password': 'password'}).json()

    {u'token': u'4ccbc35b5eb327aa82dc3b7c9747b578900f02bb'}

Add the API token to the request header::

    headers = {'Authorization': 'Token 4ccbc35b5eb327aa82dc3b7c9747b578900f02bb'}

    requests.get('http://127.0.0.1:8000/api/document_types/', headers=headers).json()

    {u'description': u'',
    u'document_type': 1,
    u'id': 19,
    u'label': u'test_document.pdf',
    u'language': u'eng'}


Use sessions to avoid having to add the headers on each request::

    session = requests.Session()

    headers = {'Authorization': 'Token 4ccbc35b5eb327aa82dc3b7c9747b578900f02bb'}

    session.headers.update(headers)

    session.get('http://127.0.0.1:8000/api/document_types/')

    {u'description': u'',
    u'document_type': 1,
    u'id': 19,
    u'label': u'test_document.pdf',
    u'language': u'eng'}
