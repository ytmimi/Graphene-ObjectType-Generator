import os
import sys
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)

from file_generator import add_imports
import pytest


def test_imports(assert_template):
    value = add_imports('import graphene', 'import datetime as dt')
    template_str = 'import graphene\nimport datetime as dt'
    assert_template(value, template_str)
