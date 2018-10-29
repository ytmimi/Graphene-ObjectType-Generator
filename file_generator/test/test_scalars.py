import os
import sys
import datetime as dt
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)

from scalars import (
    scalar, graphene_string, graphene_int, graphene_float, graphene_bool,
    graphene_id, graphene_date, graphene_datetime, graphene_time,
    graphene_json, type_from_obj
)

import pytest

class TestScalar:
    def test_only_positional_args(self):
        value = scalar('attr', 'string')
        assert value == 'attr = graphene.String()'

    def test_with_altname(self,assert_template):
        value = scalar('attr', 'string', alt_name='alt_name')
        template_str = (
        'attr = graphene.String(\n'
        "name = 'alt_name',\n"
        ')'
        )
        assert_template(value, template_str)

    def test_with_description(self, assert_template):
        value = scalar('attr', 'string', description='A description')
        template_str = (
        'attr = graphene.String(\n'
        "description = 'A description',\n"
        ')'
        )
        assert_template(value, template_str)

    def test_with_required(self, assert_template):
        value = scalar('attr', 'string', required=True)
        template_str = (
        'attr = graphene.String(\n'
        "required = True,\n"
        ')'
        )
        assert_template(value, template_str)

    def test_with_default_value(self, assert_template):
        value = scalar('attr', 'string', default_value=6)
        template_str = (
        'attr = graphene.String(\n'
        "default_value = 6,\n"
        ')'
        )
        assert_template(value, template_str)

    def test_with_all_options(self, assert_template):
        value = scalar('attr', 'string', alt_name='alt_name',
            description='A description', required=True, default_value=6)
        template_str = (
        'attr = graphene.String(\n'
        "name = 'alt_name',\n"
        "description = 'A description',\n"
        "required = True,\n"
        "default_value = 6,\n"
        ')'
        )
        assert_template(value, template_str)

class TestScalarTypes:
    def test_string(self):
        value = graphene_string(attribute_name='attr')
        assert value  == 'attr = graphene.String()'

    def test_int(self):
        value = graphene_int(attribute_name='attr')
        assert value == 'attr = graphene.Int()'

    def test_float(self):
        value = graphene_float(attribute_name='attr')
        assert value == 'attr = graphene.Float()'

    def test_bool(self):
        value = graphene_bool(attribute_name='attr')
        assert value == 'attr = graphene.Boolean()'

    def test_id(self):
        value = graphene_id(attribute_name='attr')
        assert value  == 'attr = graphene.ID()'

    def test_date(self):
        value = graphene_date(attribute_name='attr')
        assert value == 'attr = graphene.types.datetime.Date()'


    def test_datetime(self):
        value = graphene_datetime(attribute_name='attr')
        assert value == 'attr = graphene.types.datetime.DateTime()'


    def test_time(self):
        value = graphene_time(attribute_name='attr')
        assert value == 'attr = graphene.types.datetime.Time()'


    def test_json(self):
        value = graphene_json(attribute_name='attr')
        assert value  == 'attr = graphene.types.json.JSONString()'


    def test_wrong_type(self):
        with pytest.raises(ValueError) as error:
            value = scalar('attr', 'wrong')

class TestTypeFromObject:
    def test_string(self):
        value = type_from_obj(attr_name='attr', obj='a string')
        assert value  == 'attr = graphene.String()'

    def test_int(self):
        value = type_from_obj(attr_name='attr', obj=1)
        assert value == 'attr = graphene.Int()'

    def test_float(self):
        value = type_from_obj(attr_name='attr', obj=1.5)
        assert value == 'attr = graphene.Float()'

    def test_bool(self):
        value = type_from_obj(attr_name='attr', obj=True)
        assert value == 'attr = graphene.Boolean()'

    def test_date(self):
        date = dt.date(year=2018, month=1, day=1)
        value = type_from_obj(attr_name='attr', obj=date)
        assert value == 'attr = graphene.types.datetime.Date()'

    def test_time(self):
        time = dt.time(hour=1, minute=1)
        value = type_from_obj(attr_name='attr', obj=time)
        assert value == 'attr = graphene.types.datetime.Time()'

    def test_datetime(self):
        datetime = dt.datetime(year=2018, month=1, day=1)
        value = type_from_obj(attr_name='attr', obj=datetime)
        assert value == 'attr = graphene.types.datetime.DateTime()'
