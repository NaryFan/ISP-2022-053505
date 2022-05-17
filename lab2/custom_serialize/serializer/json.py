import inspect
from custom_serialize.serializer.consts import Consts
from custom_serialize.serializer_settings import *


class Json(Consts):

    def serializationn(self, obj: object, name: str, need_tabs: bool):
        obj_type = type(obj)
        if obj_type.__name__ == 'NoneType':
            return name + PARSER_DATA_NULL
        if obj_type.__name__ == 'bytes':
            return name + "b'" + obj.decode('cp866') + "'"
        if obj_type.__name__ in self.simple_type:

            if obj_type.__name__ == "str":
                res_simple = name + '"' + str(obj) + '"'
            else:
                res_simple = name + str(obj)
            if need_tabs:
                res_simple = res_simple
            return res_simple

        elif obj_type.__name__ in self.simple_list_type:

            if obj_type.__name__ == "dict":
                res_dict = name + "{"
                for key, value in obj.items():
                    if key == '__doc__':
                        continue
                    res_dict = res_dict + self.serializationn(key, "", False) + ":" + self.serializationn(value, "",
                                                                                                          False) + ','
                if (res_dict[-1] != '{'):
                    res_dict = res_dict[:-1]
                res_dict = res_dict + '}'
                return res_dict

            elif obj_type.__name__ == "tuple":
                res_tuple = name + "("
                for index in range(len(obj)):
                    res_tuple = res_tuple + self.serializationn(obj[index], "", False) + ','
                if (res_tuple[-1] != '('):
                    res_tuple = res_tuple[:-1]
                res_tuple = res_tuple + ')'
                return res_tuple

            else:
                res_list = name + "["
                for value in range(len(obj)):
                    res_list = res_list + self.serializationn(obj[value], "", False) + ','
                if (res_list[-1] != '['):
                    res_list = res_list[:-1]
                res_list = res_list + ']'
                return res_list

        elif not (obj_type.__name__ in ["builtin_function_or_method", "method-wrapper", "type"]):
            res = ""
            members = inspect.getmembers(obj)
            res = res + name + '{'
            for member in members:
                if member[0] == '__doc__':
                    continue
                res = res + str(self.serializationn(getattr(obj, member[0]), '"' + member[0] + '":', True))
                while res[-1] == ',':
                    res = res[:-1]
                if res[-1] != '{':
                    res = res + ','
            res = res[:-1]
            return res + '}'

        return ""

    def serialization(self, obj: object, class_name):
        return "{" + str(self.serializationn(obj, '"' + class_name + '":', True)) + "}"

    def check_object(self, string):
        flag = False
        res = None
        if string[0] == '{':
            flag = True
            string = string[1:]
            string, res = self.deserialization_dict(string)
        elif string[0] == '[':
            flag = True
            string = string[1:]
            string, res = self.deserialization_list(string)
        elif string[0] == '(':
            flag = True
            string = string[1:]
            string, res = self.deserialization_tuple(string)
        return flag, string, res

    def get_simple_variable(self, string):

        arr_r = [string.find(','), string.find(')'), string.find(']'), string.find('}'), string.find(':')]
        arr_r.sort()
        r = 0
        for i in arr_r:
            if i >= 0:
                r = i
                break
        res_string = string[: r]
        string = string[len(res_string):]
        if (res_string == 'None'):
            return string, None
        if res_string[0] == '"':
            return string, res_string[1:-1]
        if res_string[0] == "b":
            return string, bytes(res_string[2: -1], 'cp866')
        else:
            is_converted = False
            try:
                if not is_converted:
                    res = int(res_string)
                    is_converted = True
            except BaseException:
                is_converted = is_converted
            try:
                if not is_converted:
                    res = float(res_string)
                    is_converted = True
            except BaseException:
                is_converted = is_converted
            try:
                if not is_converted:
                    res = bytes(res_string[1:-1])
                    is_converted = True
            except BaseException:
                is_converted = is_converted
            try:
                if not is_converted:
                    res = bool(res_string)
                    is_converted = True
            except BaseException:
                is_converted = is_converted
        return string, res

    def deserialization_list(self, string: str):
        temp = list()
        while string[0] != ']' and len(string) > 0:
            flag, string, res = self.check_object(string)
            if not flag:
                string, res = self.get_simple_variable(string)
            if string[0] == ',':
                string = string[1:]
            temp.append(res)
        if len(string) > 0:
            string = string[1:]
        if len(string) > 0 and string[0] == ',':
            string = string[1:]
        return string, temp

    def deserialization_tuple(self, string: str):
        temp = tuple()
        while string[0] != ')' and len(string) > 0:
            flag, string, res = self.check_object(string)
            if not flag:
                string, res = self.get_simple_variable(string)
                if string[0] == ',':
                    string = string[1:]
            temp += tuple([res])
        if len(string) > 0:
            string = string[1:]
        if len(string) > 0 and string[0] == ',':
            string = string[1:]
        return string, temp

    def deserialization_dict(self, string: str):
        temp = dict()
        while string[0] != '}' and len(string) > 0:
            string, name = self.get_simple_variable(string)
            string = string[1:]
            flag, string, res = self.check_object(string)
            if not flag:
                string, res = self.get_simple_variable(string)
                if string[0] == ',':
                    string = string[1:]
            temp.update([(name, res)])

        if len(string) > 0:
            string = string[1:]
        if len(string) > 0 and string[0] == ',':
            string = string[1:]
        return string, temp

    def deserialization(self, string: str):
        string = string[1:]
        string, res = self.deserialization_dict(string)

        return res
