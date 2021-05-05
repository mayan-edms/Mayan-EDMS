def load_env_file(filename='config.env'):
    result = {}
    with open(file=filename) as file_object:
        for line in file_object:
            if not line.startswith('#'):
                key, value = line.strip().split('=')

                result[key] = value

    return result
