def json2dataclass(name, data: dict) -> dict:
    table = {}
    dataclass_s = \
f'''@dataclass
class {snake2pascal(name)}:\n'''

    dataclass_init = \
f'''\n    def __init__(self, data: dict):\n'''
    if len(data.values()) == 0:
        dataclass_init += \
f"""\n        pass"""
    else:
        for k, v in data.items():
            if type(v) == type(''):
                dataclass_s += '    ' + pascal2snake(k) + ': str\n'
            elif type(v) == type(0):
                dataclass_s += '    ' + pascal2snake(k) + ': int\n'
            elif type(v) == type(0.0):
                dataclass_s += '    ' + pascal2snake(k) + ': float\n'
            elif type(v) == type(True):
                dataclass_s += '    ' + pascal2snake(k) + ': bool\n'
            elif type(v) == type({}):
                dataclass_s += '    ' + pascal2snake(k) + ': ' + snake2pascal(k) + '\n'
                table.update(json2dataclass(k, v))
            elif type(v) == type([]):
                dataclass_s += '    ' + pascal2snake(k) + ': list\n'

            if table.get(snake2pascal(k)):
                dataclass_init += \
    f"""\n        self.{pascal2snake(k)} = {snake2pascal(k)}(data.get('{pascal2snake(k)}'))"""
            else:
                dataclass_init += \
    f"""\n        self.{pascal2snake(k)} = data.get('{pascal2snake(k)}')"""

    dataclass_s += '\n\n\n' + dataclass_init
    table[snake2pascal(name)] = dataclass_s
    return table


def pascal2snake(value: str) -> str:
    ret = ''
    for c in value:
        if 'A' <= c <= 'Z':
            if len(ret) > 0:
                ret += '_'
            ret += c.lower()
        else:
            ret += c
    return ret

def snake2pascal(value: str) -> str:
    ret = ''
    upper=True
    for c in value:
        if c == '_':
            upper = True
        else:
            if upper:
                upper = False
                ret += c.upper()
            else:
                ret += c
    return ret

def dict_key2snake_name(data: dict):
    if type(data) == type({}):
        keys = list(data.keys())
        for key in keys:
            dict_key2snake_name(data[key])
            if type(data[key]) == type([]):
                for i in range(len(data[key])):
                    dict_key2snake_name(data[key][i])

            data[pascal2snake(key)] = data.pop(key)

