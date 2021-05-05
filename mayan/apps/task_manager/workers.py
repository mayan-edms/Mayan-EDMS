from .classes import Worker

worker_a = Worker(name='worker_a', nice_level=0)
worker_b = Worker(name='worker_b', nice_level=2)
worker_c = Worker(name='worker_c', nice_level=15)
worker_d = Worker(concurrency=1, name='worker_d', nice_level=18)
