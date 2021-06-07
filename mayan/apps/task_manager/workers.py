from .classes import Worker

worker_a = Worker(
    maximum_tasks_per_child=100, maximum_memory_per_child=300000,
    name='worker_a', nice_level=0
)
worker_b = Worker(
    maximum_tasks_per_child=100, maximum_memory_per_child=300000,
    name='worker_b', nice_level=2
)
worker_c = Worker(
    maximum_tasks_per_child=100, maximum_memory_per_child=300000,
    name='worker_c', nice_level=15
)
worker_d = Worker(
    maximum_tasks_per_child=10, maximum_memory_per_child=300000,
    concurrency=1, name='worker_d', nice_level=18
)
