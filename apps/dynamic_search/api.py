search_list = {}

def register(model, text, field_list):
    if model in search_list:
        search_list[model]['fields'].append(field_list)
    else:
        search_list[model] = {'fields':field_list, 'text':text}
