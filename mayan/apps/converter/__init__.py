from __future__ import absolute_import

from navigation.api import register_sidebar_template
from project_tools.api import register_tool

from .links import formats_list

register_sidebar_template(['formats_list'], 'converter_file_formats_help.html')

register_tool(formats_list)
