import inspect
from custom_serialize.serializer.consts import Consts
from types import new_class, MethodType, CodeType, FunctionType
from custom_serialize.serializer_settings import *


class Parser:
    data = dict()
    args_code_type = ['co_argcount', 'co_posonlyargcount', 'co_kwonlyargcount', 'co_nlocals', 'co_stacksize',
                      'co_flags', 'co_code', 'co_consts', 'co_names', 'co_varnames', 'co_filename', 'co_name',
                      'co_firstlineno', 'co_lnotab', 'co_freevars', 'co_cellvars']

    def fill_data(self, obj):
        if inspect.isclass(obj):
            temp = dict()
            temp.update([("Type", "Class"), ("Name", obj.__name__), ("Args", dict())])
            members = inspect.getmembers(obj)
            for member in members:
                if (type(member[1]).__name__ in ["builtin_function_or_method", "method-wrapper", "wrapper_descriptor",
                                                 "mappingproxy", "method_descriptor", "getset_descriptor"]) \
                        or (member[0] in ['__class__', '__doc__']):
                    continue
                temp['Args'].update([(member[0], self.fill_data(member[1]))])
            return temp
        elif inspect.ismethod(obj) or inspect.isfunction(obj):
            return self.create_func(obj)
        else:
            if type(obj).__name__ in Consts.simple_type:
                return obj
            elif type(obj).__name__ == 'dict':
                temp = dict()
                for key in obj:
                    temp.update([(key, self.fill_data(obj[key]))])
            elif type(obj).__name__ == 'list':
                temp = []
                for index in range(len(obj)):
                    temp.append(self.fill_data(obj[index]))
            elif type(obj).__name__ == 'tuple':
                temp = tuple()
                for value in obj:
                    temp += (self.fill_data(value),)
            else:
                temp = dict()
                temp.update([('Type', 'Object'), ('Class', self.fill_data(type(obj))), ("Args", dict())])
                members = inspect.getmembers(obj)
                for member in members:
                    if (type(member[1]).__name__ in ["builtin_function_or_method", "method-wrapper",
                                                     "wrapper_descriptor",
                                                     "mappingproxy", "method_descriptor", "getset_descriptor", ]) \
                            or (member[0] in ['__class__', '__doc__', '__weakref__', '__init__', '__dict__']) or \
                            inspect.ismethod(obj) or inspect.isfunction(obj):
                        continue
                    temp['Args'].update([(member[0], self.fill_data(member[1]))])
                return temp
        return temp

    def create_func(self, obj):
        if inspect.ismethod(obj):
            type_obj = "Method"
        else:
            type_obj = "Func"
        temp = dict()
        temp.update([("Type", type_obj), ("Code", {'co_argcount': obj.__code__.co_argcount,
                                                   'co_posonlyargcount': obj.__code__.co_posonlyargcount,
                                                   'co_kwonlyargcount': obj.__code__.co_kwonlyargcount,
                                                   'co_nlocals': obj.__code__.co_nlocals,
                                                   'co_stacksize': obj.__code__.co_stacksize,
                                                   'co_flags': obj.__code__.co_flags,
                                                   'co_code': obj.__code__.co_code,
                                                   'co_consts': obj.__code__.co_consts,
                                                   'co_names': obj.__code__.co_names,
                                                   'co_varnames': obj.__code__.co_varnames,
                                                   'co_filename': obj.__code__.co_filename,
                                                   'co_name': obj.__code__.co_name,
                                                   'co_firstlineno': obj.__code__.co_firstlineno,
                                                   'co_lnotab': obj.__code__.co_lnotab,
                                                   'co_freevars': obj.__code__.co_freevars,
                                                   'co_cellvars': obj.__code__.co_cellvars
                                                   }), ("Global", dict())])
        if type(obj.__globals__).__name__ != "dict":
            return temp
        for item in temp['Code']['co_names']:
            if item == obj.__name__:
                continue
            elif item in obj.__globals__:
                temp['Global'].update([(item, self.create_func(obj.__globals__[item]))])
        return temp

    def dump(self, obj):
        self.data = self.fill_data(obj)
        return self

    def loader(self, obj, parent_class):
        if type(obj).__name__ == 'dict':
            if 'Type' in obj.keys() and len(obj.keys()) == 3:
                if obj['Type'] == 'Class':
                    temp = new_class(obj['Name'], (), ())
                    for key in obj["Args"]:
                        setattr(temp, key, self.loader(obj['Args'][key], temp))
                    return temp
                elif obj['Type'] in ['Method', "Func"]:
                    code = []
                    for item in self.args_code_type:
                        code.append(obj["Code"][item])
                    glob = {"__builtins__": __builtins__}
                    for key in obj['Global']:
                        glob[key] = self.loader(obj['Global'][key], None)
                    func = FunctionType(CodeType(*code), glob)
                    if func.__name__ in obj["Code"]['co_names']:
                        func.__globals__[func.__name__] = func
                    if parent_class is None:
                        return func
                    return MethodType(func, parent_class)
                else:
                    temp = self.loader(obj['Class'], parent_class)
                    for key in obj['Args']:
                        setattr(temp, key, self.loader(obj['Args'][key], temp))

                    return temp
            else:
                temp = dict()
                for key in obj:
                    temp.update([(key, self.loader(obj[key], parent_class))])
                return temp
        else:
            if type(obj).__name__ in Consts.simple_type:
                return obj
            elif type(obj).__name__ == 'list':
                temp = []
                for index in range(len(obj)):
                    temp.append(self.loader(obj[index], parent_class))
            else:
                temp = tuple()
                for value in obj:
                    temp += (self.loader(value, parent_class),)
            return temp

    def load(self):

        return self.loader(self.data[PARSER_DATA_NAME], None)
