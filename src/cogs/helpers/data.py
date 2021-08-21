import json

def get_data(path, key=None):
    data = {}

    try:
        open(path)
        data = json.loads(open(path).read())
    except FileNotFoundError:
        open(path, 'w').write(json.dumps({}))
    except json.decoder.JSONDecodeError:
        open(path, 'w').write(json.dumps({}))
    
    if key:
        try:
            return data[key]
        except KeyError:
            try:
                return data[str(key)]
            except:
                return 0
    else:
        return data

def set_data(path, value, key=None):
    data = get_data(path=path)

    if key:
        data[key] = value
    else:
        data = value

    open(path, 'w').write(json.dumps(data))
    return value

def append_data(path, value, key=None):
    data = get_data(path=path)

    if key:
        data[key].append(value)
    else:
        data.append(value)

    open(path, 'w').write(json.dumps(data))
    return value

def pop_data(path, key=None):
    data = get_data(path=path)
    data.pop(key)

    open(path, 'w').write(json.dumps(data))
    return path

def change_data(path, value, key=None):
    # if get_data(path=path, key=key):
    set_data(path=path, value=(get_data(path=path, key=key)+value), key=key)
    # else:
        # set_data(path=path, value=value, key=key)

def parse_boolean(text: str):
    '''Translates human language yes/no/do/dont into a boolean to improve usability'''

    if text.lower() in ['no', 'don\'t', 'dont', 'off', 'stop', '0', 'false', 'inactive', 'offline']:
        return False
    return text