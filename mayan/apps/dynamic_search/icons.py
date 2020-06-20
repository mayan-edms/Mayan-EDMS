from mayan.apps.appearance.classes import Icon

icon_search = Icon(
    driver_name='fontawesome', symbol='search'
)
icon_search_advanced = Icon(
    driver_name='fontawesome', symbol='search-plus'
)
icon_search_again = Icon(
    driver_name='fontawesome', symbol='sync'
)
icon_search_backend_reindex = Icon(
    driver_name='fontawesome-layers', data=[
        {
            'class': 'fas fa-circle',
            'transform': 'down-3 right-10',
            'mask': 'fas fa-search'
        },
        {'class': 'far fa-circle', 'transform': 'down-3 right-10'},
        {'class': 'fas fa-search', 'transform': 'flip-h left-3'},
        {'class': 'fas fa-hammer', 'transform': 'shrink-4 down-3 right-10'}
    ]
)
icon_search_submit = Icon(
    driver_name='fontawesome', symbol='search'
)
