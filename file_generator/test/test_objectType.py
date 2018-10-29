import os
import sys
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)

import objectType as ot
import pytest

FIELDS = [
'string = graphene.String()',
'int = graphene.Int()',
'float = graphene.Float()',
'bool = graphene.Boolean()',
]

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
        'string = graphene.String()\n'
        'int = graphene.Int()\n'
        'float = graphene.Float()\n'
        'bool = graphene.Boolean()'
        )
        assert_template(value, template_str)
