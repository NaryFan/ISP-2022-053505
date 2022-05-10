from custom_serialize.serializer.json import Json
from custom_serialize.serializer.yaml import Yaml
from custom_serialize.serializer.toml import Toml


test_dict = {
    'v_int': 1,
    'v_float': 1.23,
    'v_bool': True,
    'v_tuple': (1, 2, 3),
    'v_dict': {'1': 1, '2': 2, '3': 3, '4': 4},
    'v_list': [1, [1, 'ggggg', True], 3, 4]
}
parsers = [Json(), Yaml(), Toml()]


def test_json():
    string = parsers[0].serialization(test_dict, 'Parser_Data')
    obj = parsers[0].deserialization(string)
    assert obj['Parser_Data'] == test_dict

    assert parsers[0].deserialization(parsers[0].serialization(test_dict['v_int'], 'Parser_Data'))['Parser_Data'] == \
           test_dict['v_int']
    assert parsers[0].deserialization(parsers[0].serialization(test_dict['v_float'], 'Parser_Data'))['Parser_Data'] == \
           test_dict['v_float']
    assert parsers[0].deserialization(parsers[0].serialization(test_dict['v_bool'], 'Parser_Data'))['Parser_Data'] == \
           test_dict['v_bool']
    assert parsers[0].deserialization(parsers[0].serialization(test_dict['v_tuple'], 'Parser_Data'))['Parser_Data'] == \
           test_dict['v_tuple']
    assert parsers[0].deserialization(parsers[0].serialization(test_dict['v_dict'], 'Parser_Data'))['Parser_Data'] == \
           test_dict['v_dict']
    assert parsers[0].deserialization(parsers[0].serialization(test_dict['v_list'], 'Parser_Data'))['Parser_Data'] == \
           test_dict['v_list']


def test_yaml():
    string = parsers[1].serialization(test_dict, 'Parser_Data')
    obj = parsers[1].deserialization(string)
    assert obj['Parser_Data'] == test_dict

    assert parsers[1].deserialization(parsers[1].serialization(test_dict['v_int'], 'Parser_Data'))['Parser_Data'] == \
           test_dict['v_int']
    assert parsers[1].deserialization(parsers[1].serialization(test_dict['v_float'], 'Parser_Data'))['Parser_Data'] == \
           test_dict['v_float']
    assert parsers[1].deserialization(parsers[1].serialization(test_dict['v_bool'], 'Parser_Data'))['Parser_Data'] == \
           test_dict['v_bool']
    assert parsers[1].deserialization(parsers[1].serialization(test_dict['v_tuple'], 'Parser_Data'))['Parser_Data'] == \
           test_dict['v_tuple']
    assert parsers[1].deserialization(parsers[1].serialization(test_dict['v_dict'], 'Parser_Data'))['Parser_Data'] == \
           test_dict['v_dict']
    assert parsers[1].deserialization(parsers[1].serialization(test_dict['v_list'], 'Parser_Data'))['Parser_Data'] == \
           test_dict['v_list']


string = parsers[2].serialization(test_dict, 'Parser_Data')
obj = parsers[2].deserialization(string)
pass


def test_toml():
    string = parsers[2].serialization(test_dict, 'Parser_Data')
    obj = parsers[2].deserialization(string)
    assert obj['Parser_Data'] == test_dict

    assert parsers[2].deserialization(parsers[2].serialization(test_dict['v_int'], 'Parser_Data'))['Parser_Data'] == \
           test_dict['v_int']
    assert parsers[2].deserialization(parsers[2].serialization(test_dict['v_float'], 'Parser_Data'))['Parser_Data'] == \
           test_dict['v_float']
    assert parsers[2].deserialization(parsers[2].serialization(test_dict['v_bool'], 'Parser_Data'))['Parser_Data'] == \
           test_dict['v_bool']
    assert parsers[2].deserialization(parsers[2].serialization(test_dict['v_tuple'], 'Parser_Data'))['Parser_Data'] == \
           test_dict['v_tuple']
    assert parsers[2].deserialization(parsers[2].serialization(test_dict['v_dict'], 'Parser_Data'))['Parser_Data'] == \
           test_dict['v_dict']
    assert parsers[2].deserialization(parsers[2].serialization(test_dict['v_list'], 'Parser_Data'))['Parser_Data'] == \
           test_dict['v_list']


pass
