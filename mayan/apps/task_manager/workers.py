from mayan.settings.literals import (
    MAYAN_WORKER_A_CONCURRENCY, MAYAN_WORKER_A_MAX_MEMORY_PER_CHILD,
    MAYAN_WORKER_A_MAX_TASKS_PER_CHILD, MAYAN_WORKER_B_CONCURRENCY,
    MAYAN_WORKER_B_MAX_MEMORY_PER_CHILD, MAYAN_WORKER_B_MAX_TASKS_PER_CHILD,
    MAYAN_WORKER_C_CONCURRENCY, MAYAN_WORKER_C_MAX_MEMORY_PER_CHILD,
    MAYAN_WORKER_C_MAX_TASKS_PER_CHILD, MAYAN_WORKER_D_CONCURRENCY,
    MAYAN_WORKER_D_MAX_MEMORY_PER_CHILD, MAYAN_WORKER_D_MAX_TASKS_PER_CHILD
)

from .classes import Worker

worker_a = Worker(
    concurrency=MAYAN_WORKER_A_CONCURRENCY,
    maximum_memory_per_child=MAYAN_WORKER_A_MAX_MEMORY_PER_CHILD,
    maximum_tasks_per_child=MAYAN_WORKER_A_MAX_TASKS_PER_CHILD,
    name='worker_a', nice_level=0
)
worker_b = Worker(
    concurrency=MAYAN_WORKER_B_CONCURRENCY,
    maximum_memory_per_child=MAYAN_WORKER_B_MAX_MEMORY_PER_CHILD,
    maximum_tasks_per_child=MAYAN_WORKER_B_MAX_TASKS_PER_CHILD,
    name='worker_b', nice_level=2
)
worker_c = Worker(
    concurrency=MAYAN_WORKER_C_CONCURRENCY,
    maximum_memory_per_child=MAYAN_WORKER_C_MAX_MEMORY_PER_CHILD,
    maximum_tasks_per_child=MAYAN_WORKER_C_MAX_TASKS_PER_CHILD,
    name='worker_c', nice_level=15
)
worker_d = Worker(
    concurrency=MAYAN_WORKER_D_CONCURRENCY,
    maximum_memory_per_child=MAYAN_WORKER_D_MAX_MEMORY_PER_CHILD,
    maximum_tasks_per_child=MAYAN_WORKER_D_MAX_TASKS_PER_CHILD,
    name='worker_d', nice_level=18
)
