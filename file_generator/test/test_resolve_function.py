import os
import sys
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)

from resolve_function import resolver_func
import pytest


def test_resolve_template(assert_template):
    result = resolver_func('some_attribute')
    template_str = (
    'def resolve_some_attribute(self, info, *args, **kwargs):\n'
    'pass'
    )
    assert_template(result, template_str)
