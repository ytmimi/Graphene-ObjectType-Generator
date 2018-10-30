import pytest
import datetime as dt

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

@pytest.fixture(scope='module')
def date():
    '''Needed a fixture to mock a random date object '''
    return dt.date(year=2018, month=1, day=1)

@pytest.fixture(scope='module')
def time():
    '''Needed a fixture to mock a random date object '''
    return dt.time(hour=1, minute=1)

@pytest.fixture(scope='module')
def datetime():
    '''Needed a fixture to mock a random date object '''
    return dt.datetime(year=2018, month=1, day=1)
