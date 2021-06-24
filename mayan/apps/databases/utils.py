def instance_list_to_queryset(instance_list):
    manager = instance_list[0]._meta.default_manager

    return manager.filter(pk__in=[instance.pk for instance in instance_list])
