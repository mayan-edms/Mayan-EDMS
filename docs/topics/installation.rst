Installation
============

The easiest way to use Mayan EDMS is by using the official Docker_ image.
Make sure Docker is properly installed and working before attempting to install
Mayan EDMS.

Hardware requirements
---------------------

- 2 Gigabytes of RAM (1 Gigabyte if OCR is turned off).
- Multiple core CPU (64 bit, faster than 1 GHz recommended).

Docker procedure
----------------

Docker is a computer program that performs operating-system-level
virtualization also known as containerization. It allows independent
"containers" to run within a single Linux instance, avoiding the overhead
of starting and maintaining virtual machines (VMs).

Docker can be installed using their automated script::

    wget -qO- https://get.docker.com/ | sh

This installs the latest versions of Docker. If you don't want run an automated
script follow the instructions outlined in their documentation: https://docs.docker.com/install/

Once the Docker installtion is finished, proceed to the link below to install
the Docker image for Mayan EDMS.

Docker image chapter: :ref:`docker`

Direct installation
-------------------

For users with knowledge of Python, Django, Ubuntu, and databases.

Advanced deployment chapter: :ref:`deploying`


.. _Docker: https://www.docker.com/
