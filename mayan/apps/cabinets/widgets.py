from django.utils.html import format_html


def jstree_data(node, selected_node):
    result = []

    result.append('{')
    result.append(format_html('"text": "{}",', node.label))
    result.append(
        '"state": {{ "opened": true, "selected": {} }},'.format(
            'true' if node == selected_node else 'false'
        )
    )
    result.append(
        '"data": {{ "href": "{}" }},'.format(node.get_absolute_url())
    )

    children = node.get_children().order_by('label',)

    if children:
        result.append('"children" : [')
        for child in children:
            result.extend(jstree_data(node=child, selected_node=selected_node))

        result.append(']')

    result.append('},')

    return result
