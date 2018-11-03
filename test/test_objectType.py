import os
import sys

import objectType as ot
import pytest

FIELDS = [
'str = graphene.String()',
'int = graphene.Int()',
'float = graphene.Float()',
'bool = graphene.Boolean()',
]

# taken from the old scalar tests
def test_inspect_type(date, datetime, time):
    objects = ['some_strings', 1, 1.5, True, [], {}, date, datetime, time]
    expected = ['str', 'int', 'float', 'bool', 'list', 'dict', 'date', 'datetime', 'time']
    for obj, exp in zip(objects, expected):
        assert inspect_type(obj) == exp


class TestCeateObjectType:
    def test_no_fields(self, assert_template):
        value = ot.create_objectType(class_name='Math')
        template_str = (
        'class Math(graphene.ObjectType):\n'
        'pass'
        )
        assert_template(value, template_str)

    def test_with_fields(self, assert_template):
        value = ot.create_objectType(class_name='Math', fields=FIELDS)
        print()
        print(value)
        template_str = (
        'class Math(graphene.ObjectType):\n'
        'str = graphene.String()\n'
        'int = graphene.Int()\n'
        'float = graphene.Float()\n'
        'bool = graphene.Boolean()'
        )
        assert_template(value, template_str)


@pytest.fixture
def data_dict(date, datetime, time):
    return {
        'one':'string',
        'two':1,
        'three':2.5,
        'four':True,
        'five':date,
        'six':datetime,
        'seven':time,
        'eight':[1, 2, 3],
    }

@pytest.fixture
def data_dict_with_dict(data_dict):
    return {**data_dict, 'nine':{'ten':10, 'eleven':11}}


def test_objectType_from_dict(assert_template, data_dict):
    result = ot.objectTypes_from_dict('Test', data_dict)
    assert isinstance(result, list)
    assert len(result) == 1
    template_str = (
        'class Test(graphene.ObjectType):\n'
        'one = graphene.String()\n'
        'two = graphene.Int()\n'
        'three = graphene.Float()\n'
        'four = graphene.Boolean()\n'
        'five = graphene.types.datetime.Date()\n'
        'six = graphene.types.datetime.DateTime()\n'
        'seven = graphene.types.datetime.Time()\n'
        'eight = graphene.List(graphene.Int,)'
    )
    assert_template(result[0], template_str)


def test_objectType_from_dict_with_dict(assert_template, data_dict_with_dict):
    result = ot.objectTypes_from_dict('Test', data_dict_with_dict)
    assert isinstance(result, list)
    assert len(result) == 2
    template_str1 = (
        'class Test(graphene.ObjectType):\n'
        'one = graphene.String()\n'
        'two = graphene.Int()\n'
        'three = graphene.Float()\n'
        'four = graphene.Boolean()\n'
        'five = graphene.types.datetime.Date()\n'
        'six = graphene.types.datetime.DateTime()\n'
        'seven = graphene.types.datetime.Time()\n'
        'eight = graphene.List(graphene.Int,)\n'
        'nine = graphene.Field(NineType,)\n'
        '\n'
        'def resolve_nine(self, info, *args, **kwargs):\n'
        'pass'
    )
    assert_template(result[1], template_str1)
    template_str2 = (
        'class NineType(graphene.ObjectType):\n'
        'ten = graphene.Int()\n'
        'eleven = graphene.Int()'
    )
    assert_template(result[0], template_str2)

@pytest.fixture(scope='module')
def data_list():
    '''
    retutns a list of dicts
    '''
    return [{'one':1, 'two':2, 'three':{'four':4, 'five':5}}]

def test_objectType_from_list(data_list, assert_template):
    result = ot.objectTypes_from_list('number', data_list)
    assert isinstance(result, list)
    assert len(result) == 3
    template_str1 = (
    'class ThreeType(graphene.ObjectType):\n'
    'four = graphene.Int()\n'
    'five = graphene.Int()'
    )
    assert_template(result[0], template_str1)
    template_str2 = (
    'class NumberType(graphene.ObjectType):\n'
    'one = graphene.Int()\n'
    'two = graphene.Int()\n'
    'three = graphene.Field(ThreeType,)\n'
    '\n'
    'def resolve_three(self, info, *args, **kwargs):\n'
    'pass'
    )
    assert_template(result[1], template_str2)
    template_str3 = (
    'class Query(graphene.ObjectType):\n'
    'number = graphene.List(NumberType,)\n'
    '\n'
    'def resolve_number(self, info, *args, **kwargs):\n'
    'pass'
    )
    assert_template(result[2], template_str3)

    print()
    for res in result:
        print(res)
