![Logo](https://github.com/rosarior/mayan/raw/master/docs/_static/mayan_logo_landscape_black.jpg)

Mayan EDMS
==========

Open source, Django based document management system with custom metadata
indexing, file serving integration, tagging, digital signature verification,
text parsing and OCR capabilities.

[Website](http://www.mayan-edms.com)

[Video demostration](http://bit.ly/pADNXv)

[Documentation](http://readthedocs.org/docs/mayan/en/latest/)

[Translations](https://www.transifex.net/projects/p/mayan-edms/)

[Mailing list (via Google Groups)](http://groups.google.com/group/mayan-edms)


Quick install
-------------
To bootstrap **Mayan EDMS** via the fabfile without having to clone the
entire repository, run the following command, replacing the part that
reads: <Your MySQL root password> with your current MySQL root password
or the MySQL root password you plan to assign to it, during the MySQL
installation when executing the fabfile.

- Debian or Ubuntu:

    cd /tmp && sudo apt-get install -y fabric wget tar gzip && wget https://github.com/rosarior/mayan/raw/master/contrib/fabfile.tar.gz -O - | tar -xvzf - && echo "database_manager_admin_password=&lt;Your MySQL root password&gt;" > ~/.fabricrc && fab -H localhost install
    
- Fedora:

    cd /tmp && sudo yum install -y fabric wget tar gzip && wget https://github.com/rosarior/mayan/raw/master/contrib/fabfile.tar.gz -O - | tar -xvzf - && echo "database_manager_admin_password=&lt;Your MySQL root password&gt;" > ~/.fabricrc && fab -H localhost install


License
-------
This project is open sourced under [GNU GPL Version 3](http://www.gnu.org/licenses/gpl-3.0.html).


Author
------
Roberto Rosario - [Twitter](http://twitter.com/#siloraptor) [E-mail](mailto://roberto.rosario@mayan-edms.com)


Donations
---------
Please [donate](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=W6LMMZHTNUJ6L) if you are willing to support the further development of this project.

