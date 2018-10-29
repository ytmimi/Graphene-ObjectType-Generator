import pytest

@pytest.fixture(scope='module')
def assert_template():
    def test_func(value, template_str):
        '''
        Assert that the number of lines in the the generated text
        and the expected output is the same. Then checks that the value
        of each line is the same.
        '''
        value_lines = list(map(lambda x: x.strip(), value.split('\n')))
        templte_lines = list(map(lambda x: x.strip(), template_str.split('\n')))
        assert len(value_lines) == len(templte_lines)
        for value, temp in zip(value_lines, templte_lines):
            assert value == temp
    return test_func
