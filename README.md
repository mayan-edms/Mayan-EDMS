[![pypi][pypi]][pypi-url]
[![builds][builds]][builds-url]
[![coverage][cover]][cover-url]
![python][python]
![license][license]

[pypi]: http://img.shields.io/pypi/v/mayan-edms.svg
[pypi-url]: http://badge.fury.io/py/mayan-edms

[builds]: https://gitlab.com/mayan-edms/mayan-edms/badges/master/build.svg
[builds-url]: https://gitlab.com/mayan-edms/mayan-edms/pipelines

[cover]: https://codecov.io/gitlab/mayan-edms/mayan-edms/coverage.svg?branch=master
[cover-url]: https://codecov.io/gitlab/mayan-edms/mayan-edms?branch=master

[python]: https://img.shields.io/pypi/pyversions/mayan-edms.svg
[python-url]: https://img.shields.io/pypi/l/mayan-edms.svg?style=flat

[license]: https://img.shields.io/pypi/l/mayan-edms.svg?style=flat
[license-url]: https://img.shields.io/pypi/l/mayan-edms.svg?style=flat


<div align="center">
  <a href="http://www.mayan-edms.com">
    <img width="200" heigth="200" src="https://gitlab.com/mayan-edms/mayan-edms/raw/master/docs/_static/mayan_logo.png">
  </a>
  <br>
  <br>
  <p>
    Mayan EDMS is a document management system. Its main purpose is to store,
    introspect, and categorize files, with a strong emphasis on preserving the
    contextual and business information of documents. It can also OCR, preview,
    label, sign, send, and receive thoses files. Other features of interest
    are its workflow system, role based access control, and REST API.
  <p>

<p align="center">
    <img src="https://gitlab.com/mayan-edms/mayan-edms/raw/master/docs/_static/overview.gif">
</p>

</div>

<h2 align="center">Installation</h2>

The installation procedure uses the <a href="https://www.docker.com">Docker container manager (docker.com)</a>. Make sure Docker is properly installed and working before attempting to install Mayan EDMS.

Step 1- Initialize the installation

```bash
docker run --rm -v mayan_media:/var/lib/mayan \
-v mayan_settings:/etc/mayan mayanedms/mayanedms mayan:init
```

Step 2- Deploy a container

```bash
docker run -d --name mayan-edms --restart=always -p 80:80 \
-v mayan_media:/var/lib/mayan -v mayan_settings:/etc/mayan mayanedms/mayanedms
```

Step 3- Open a browser and go to http://localhost


<h2 align="center">Important links</h2>


- [Homepage](http://www.mayan-edms.com)
- [Videos](https://www.youtube.com/channel/UCJOOXHP1MJ9lVA7d8ZTlHPw)
- [Documentation](http://mayan.readthedocs.io/en/stable/)
- [Paid support](http://www.mayan-edms.com/providers/)
- [Community forum](https://groups.google.com/forum/#!forum/mayan-edms)
- [Community forum archive](http://mayan-edms.1003.x6.nabble.com/)
- [Source code, issues, bugs](https://gitlab.com/mayan-edms/mayan-edms)
- [Plug-ins, other related projects](https://gitlab.com/mayan-edms/)
- [Translations](https://www.transifex.com/rosarior/mayan-edms/)

