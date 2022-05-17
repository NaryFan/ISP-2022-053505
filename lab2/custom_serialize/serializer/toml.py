import pytomlpp as toml
from custom_serialize.serializer_settings import *


class Toml:

    def serialization(self, obj, parser_name: str):
        self.del_null(obj)
        return toml.dumps({parser_name: obj})

    def deserialization(self, s: str):
        res = toml.loads(s)
        self.insert_null(res)
        return res

    def del_null(self, obj):

        if obj is None:
            obj = PARSER_DATA_NULL

        elif type(obj).__name__ == 'dict':
            for key, value in obj.items():
                obj[key] = self.del_null(value)

        elif type(obj).__name__ == 'list':
            for i in range(len(obj)):
                obj[i] = self.del_null(obj[i])

        elif type(obj).__name__ == 'tuple':
            obj = list(obj)
            for i in range(len(obj)):
                obj[i] = self.del_null(obj[i])
        return obj

    def insert_null(self, obj):

        if obj == PARSER_DATA_NULL:
            return None

        elif type(obj).__name__ == 'dict':
            for key, value in obj.items():
                if value == PARSER_DATA_NULL:
                    obj[key] = None
                else:
                    self.insert_null(value)

        elif type(obj).__name__ == 'list':
            for i in range(len(obj)):
                obj[i] = self.insert_null(obj[i])

        return obj
