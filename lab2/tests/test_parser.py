from custom_serialize.serializer.serializer import Parser
from custom_serialize.serializer_settings import *

test_dict = {
    'v_int': 1,
    'v_float': 1.23,
    'v_bool': True,
    'v_tuple': (1, 2, 3),
    'v_dict': {'1': 1, '2': 2, '3': 3, '4': 4},
    'v_list': [1, [1, 'fsdsd', True], 3, 4]
}


class InnerClass(object):
    qwe = "qwe"

    def equal(self, obj):
        return self.qwe == obj.qwe


class ParentClass(object):
    def __init__(self):
        self.vint = 123

    v_qwe = InnerClass()
    v_int = 1
    v_float = 1.23
    v_bool = True
    v_tuple = (1, 2, 3)
    v_dict = {'1': 1, '2': 2, '3': 3, '4': 4}
    v_list = [1, [1, 'fsdsd', True], 3, 4]
    v_class = InnerClass


class ChildClass(ParentClass):
    vstr = "1234567890"

    def insert_in_method(self, k: int, f):
        return self.insert_in_function(k + self.v_int, f)

    def insert_in_function(self, k: int, f):
        return f(k + function(1))

    def equal(self, obj):
        return self.vint == obj.vint and self.v_int == obj.v_int and self.v_qwe.equal(obj.v_qwe) and \
               self.v_bool == obj.v_bool and self.v_dict == obj.v_dict and self.v_float == obj.v_float and \
               self.v_tuple == obj.v_tuple and self.vstr == obj.vstr and self.v_class().equal(obj.v_class())


def function(a: int):
    return a ** a


def rec(steps: int, add: int):
    if steps <= 0:
        return 0
    return rec(steps - 1, add) + add


def rec_and_func(steps, a: int):
    return rec(steps, function(a))


par = Parser()


def test_parser_simple():
    assert par.dump({PARSER_DATA_NAME: test_dict}).load() == test_dict


def test_parser_classes():
    par.dump({PARSER_DATA_NAME: ChildClass()})
    obj = par.load()
    assert ChildClass().equal(obj)
    assert obj.insert_in_method(1, function) == function(3)


def test_parser_functions():
    par.dump({PARSER_DATA_NAME: function})
    obj = par.load()
    assert obj(3) == function(3)

    par.dump({PARSER_DATA_NAME: rec})
    obj = par.load()
    assert obj(3, 3) == rec(3, 3)

    par.dump({PARSER_DATA_NAME: rec_and_func})
    obj = par.load()
    assert obj(3, 2) == rec_and_func(3, 2)
