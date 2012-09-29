from __future__ import absolute_import

from icons.literals import (LORRY_GO, LORRY_DELETE, HOURGLASS, COG, COG_DELETE,
    COG_ERROR, COG_ADD, CONTROL_PLAY_BLUE, CONTROL_STOP_BLUE, COG_HOURGLASS)
from icons import Icon

icon_node_workers = Icon(LORRY_GO)
icon_tool_link = Icon(HOURGLASS)
icon_job_queues = Icon(HOURGLASS)
icon_job_queue_items_pending = Icon(COG_HOURGLASS)
icon_job_queue_items_error = Icon(COG_ERROR)
icon_job_queue_items_active = Icon(COG)
icon_job_queue_start = Icon(CONTROL_PLAY_BLUE)
icon_job_queue_stop = Icon(CONTROL_STOP_BLUE)
icon_job_requeue = Icon(COG_ADD)
icon_job_delete = Icon(COG_DELETE)
icon_worker_terminate = Icon(LORRY_DELETE)
