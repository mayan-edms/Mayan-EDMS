**********
Scaling up
**********

The default installation method fits most use cases. If you use case requires
more speed or capacity here are some suggestion that can help you improve the
performance of your installation.


Change the database manager
===========================

Use PostgreSQL or MySQL as the database manager.
Tweak the memory setting of the database manager to increase memory allocation.
More PostgreSQL specific examples are available in their wiki page:
https://wiki.postgresql.org/wiki/Performance_Optimization


Increase the number of Gunicorn workers
=======================================

The Gunicorn workers process HTTP requests and affect the speed at which the
website responds.

If you are using the Docker image, change the value of the
``MAYAN_GUNICORN_WORKERS`` environment variable (check the Docker image chapter:
:ref:`docker_environment_variables`). Normally this variable defaults to 2.
Increase this number to match the number of CPU cores + 1.

If you are using the direct deployment methods, change the line that reads::

    command = /opt/mayan-edms/bin/gunicorn -w 2 mayan.wsgi --max-requests 500 --max-requests-jitter 50 --worker-class gevent --bind 0.0.0.0:8000 --timeout 120

And increase the value of the ``-w 2`` argument. This line is found in the
``[program:mayan-gunicorn]`` section of the supervisor configuration file.


Background task processing
==========================

The Celery workers are system processes that take care of the background
tasks requested by the frontend interactions like document image rendering
and periodic tasks like OCR. There are several dozen tasks defined in the code.
These tasks are divided into queues based on the app of the relationship
between the tasks. The queues by default are divided into three groups
based on the speed at which they need to be processed. The document page
image rendering for example is categorized as a high volume, short duration
task. The OCR is a high volume, long duration task. Email checking is a
low volume, medium duration tasks. It is not advisable to have the same
worker processing OCR to process image rendering too. If the worker is
processing several OCR tasks it will not be able to provide fast images
when an user is browsing the user interface. This is why by default the
queues are split into 3 workers: fast, medium, and slow. Each worker will handle
queues based on the latency required by each queue group.


Optimizations
-------------

* Increase the number of workers and redistribute the queues among them
  (only possible with direct deployments).
* Launch more workers to service a queue. For example for faster document
  image generation launch 2 workers to process the converter queue only
  possible with direct deployments).
* By default each worker process uses 1 thread. You can increase the thread
  count of each worker process with the Docker environment options:

  * ``MAYAN_WORKER_FAST_CONCURRENCY``
  * ``MAYAN_WORKER_MEDIUM_CONCURRENCY``
  * ``MAYAN_WORKER_SLOW_CONCURRENCY``

* If using direct deployment, increase the value of the ``--concurrency=1``
  argument of each worker in the supervisor file. You can also remove this
  argument and let the Celery algorithm choose the number of threads to
  launch. Usually this defaults to the number of CPU cores + 1.


Change the message broker
=========================
Messages are the method of communication between front end interactive code
and background tasks. In this regard messages can be thought as homologous
to tasks requests. Improving how many messages can be sent, stored and
sorted will impact the number of tasks the system can handle. To save on
memory, the basic deployment method and the Docker image default to using
Redis as a message broker. To increase capacity and reduce volatility of
messages (pending tasks are not lost during shutdown) use RabbitMQ to
shuffle messages.

For direct installs refer to the :ref:`deployment_advanced` documentation
section for the required changes.

For the Docker image, launch a separate RabbitMQ container
(https://hub.docker.com/_/rabbitmq/)::

    docker run -d --name mayan-edms-rabbitmq -e RABBITMQ_DEFAULT_USER=mayan -e RABBITMQ_DEFAULT_PASS=mayanrabbitmqpassword -e RABBITMQ_DEFAULT_VHOST=mayan rabbitmq:3

Pass the MAYAN_BROKER_URL environment variable (https://kombu.readthedocs.io/en/latest/userguide/connections.html#connection-urls)
to the Mayan EDMS container so that it uses the RabbitMQ container the
message broker::

    -e MAYAN_BROKER_URL="amqp://mayan:mayanrabbitmqpassword@localhost:5672/mayan",

When tasks finish, they leave behind a return status or the result of a
calculation, these are stored for a while so that whoever requested the
background task, is able retrieve the result. These results are stored in the
result storage. By default a Redis server is launched inside the Mayan EDMS
container. You can launch a separate Docker Redis container and tell the Mayan
EDMS container to use this via the ``MAYAN_CELERY_RESULT_BACKEND`` environment
variable. The format of this variable is explained here: http://docs.celeryproject.org/en/3.1/configuration.html#celery-result-backend


Deployment type
===============

Docker provides a faster deployment and the overhead is not high on modern
systems. It is however memory and CPU limited by default and you need to
increase this limits. The settings to change the container resource limits
are here: https://docs.docker.com/config/containers/resource_constraints/#limit-a-containers-access-to-memory

For the best performance possible use the advanced deployment method on a
host dedicated to serving only Mayan EDMS.


Storage
=======

For best input and output speed use a block based local filesystem on an
SSD drive for the ``/media`` sub folder. The location of the ``/media`` folder
will be specified by the ``MEDIA_ROOT`` setting.

If capacity is your bottom line, switch to an
:doc:`object storage <../chapters/object_storage>` system.


Use additional hosts
====================

When one host is not enough you can use multiple hosts and share the load.
Make sure that all hosts share the ``/media`` folder as specified by the
``MEDIA_ROOT`` setting, also the database, the broker, and the result storage.
One setting that needs to be changed in this configuration is the lock
manager backend.

Resource locking is a technique to avoid two processes or tasks to modify
the same resource at the same time causing a race condition. Mayan EDMS uses
its own lock manager. By default the lock manager with use a simple file
based lock backend ideal for single host installations. For multiple hosts
installation the database backend must be used in other to coordinate the
resource locks between the different hosts over a share data medium. This is
accomplished by modifying the environment variable ``LOCK_MANAGER_BACKEND`` in
both the direct deployment or the Docker image. Use the value
``lock_manager.backends.model_lock.ModelLock`` to switch to the database
resource lock backend. If you can also write your own lock manager backend
for other data sharing mediums with better performance than a relational
database like Redis, Memcached, Zoo Keeper.
