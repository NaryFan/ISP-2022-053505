from custom_serialize.serializer.serializer import Parser
from custom_serialize.serializer.json import Json
from custom_serialize.serializer.yaml import Yaml
from custom_serialize.serializer.toml import Toml
from custom_serialize.serializer_settings import *

main_parser = Parser()


def get_format(format_parser: str):
    if format_parser == 'json':
        return Json()
    elif format_parser == 'yaml':
        return Yaml()
    elif format_parser == 'toml':
        return Toml()
    else:
        raise ValueError('Unknown parser. You may have entered the wrong name for the parser')


def dump(obj, format_parser: str, file_path: str):
    f = open(file_path, 'w')
    f.write(get_format(format_parser).serialization(main_parser.dump(obj).data, PARSER_DATA_NAME))


def dumps(obj, format_parser: str):
    return get_format(format_parser).serialization(main_parser.dump(obj).data, PARSER_DATA_NAME)


def load(file_path: str, format_parser: str):
    main_parser.data = get_format(format_parser).deserialization(open(file_path, 'r').read())
    return main_parser.load()


def loads(string: str, format_parser: str):
    main_parser.data = (get_format(format_parser).deserialization(string))
    return main_parser.load()
