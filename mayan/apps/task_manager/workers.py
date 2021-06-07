from .classes import Worker

worker_a = Worker(
    maximum_memory_per_child=300000, maximum_tasks_per_child=100,
    name='worker_a', nice_level=0
)
worker_b = Worker(
    maximum_memory_per_child=300000, maximum_tasks_per_child=100,
    name='worker_b', nice_level=2
)
worker_c = Worker(
    maximum_memory_per_child=300000, maximum_tasks_per_child=100,
    name='worker_c', nice_level=15
)
worker_d = Worker(
    concurrency=1, maximum_memory_per_child=300000,
    maximum_tasks_per_child=10, name='worker_d', nice_level=18
)
