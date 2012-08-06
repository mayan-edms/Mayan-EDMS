from navigation.api import bind_links

from .links import maintenance_menu

tools = {}


class MaintenanceNamespace(object):
    namespaces = {}
    tools_by_id = {}

    @classmethod
    def tool_all(cls):
        tool_list = []
        for namespace in cls.all():
            for tool in namespace.tools:
                tool_list.append(tool)
                
        return tool_list

    @classmethod
    def tool_get(cls, id):
        return MaintenanceNamespace.tools_by_id[id]

    @classmethod
    def all(cls):
        return MaintenanceNamespace.namespaces.keys()

    def __init__(self, label):
        self.label = label
        self.tools = []
        MaintenanceNamespace.namespaces[self] = self

    def create_tool(self, link):
        tool = MaintenanceTool(self, link)
        self.add_tool(tool)
        return tool

    def add_tool(self, tool_instance):
        self.tools.append(tool_instance)
        tool_instance.id = len(MaintenanceNamespace.tools_by_id) + 1
        MaintenanceNamespace.tools_by_id[tool_instance.id] = tool_instance
        bind_links([tool_instance.link.view], maintenance_menu, menu_name='secondary_menu')

    def __unicode__(self):
        return unicode(self.label)


class MaintenanceTool(object):
    def __init__(self, namespace, link):
        self.namespace = namespace
        self.link = link

    def __unicode__(self):
        return unicode(self.link.text)
