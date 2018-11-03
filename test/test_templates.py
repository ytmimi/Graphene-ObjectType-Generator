from objecttype_generator import templates
import pytest

def test_resolver(assert_template):
    result = templates.resolver('attr_name')
    expected = ('''
    def resolve_attr_name(self, info, *args, **kwargs):
        pass
    ''').strip() #get rid of leading and trailing white space
    assert_template(result, expected)

@pytest.fixture(scope='module')
def object_list():
    return ['str', 'int', 'float', 'bool', 'date', 'datetime', 'time', 'json']

@pytest.fixture(scope='module')
def attribute():
    return 'some_attr'


class TestGrapheneScalar:
    def test_only_positional_args(self):
        #scalar takes in an attribute_name and a type_
        result = templates.graphene_scalar('attr', 'str')
        assert result == 'attr = graphene.String()'

    def test_with_altname(self, assert_template):
        result = templates.graphene_scalar('attr', 'str', alt_name='alt_name')
        expected = ('''
        attr = graphene.String(
            name = 'alt_name',
        )''').strip()
        assert_template(result, expected)

    def test_with_description(self, assert_template):
        result = templates.graphene_scalar('attr', 'str', description='A description')
        expected = ('''
        attr = graphene.String(
            description = 'A description',
        )''').strip()
        assert_template(result, expected)

    def test_with_required(self, assert_template):
        result = templates.graphene_scalar('attr', 'str', required=True)
        expected = ('''
        attr = graphene.String(
            required = True,
        )''').strip()
        assert_template(result, expected)

    def test_with_default_value(self, assert_template):
        result = templates.graphene_scalar('attr', 'str', default_value=6)
        expected = ('''
        attr = graphene.String(
            default_value = 6,
        )''').strip()
        assert_template(result, expected)

    def test_with_all_options(self, assert_template):
        result = templates.graphene_scalar('attr', 'str', alt_name='alt_name',
            description='A description', required=True, default_value=6)
        expected = ('''
        attr = graphene.String(
            name = 'alt_name',
            description = 'A description',
            required = True,
            default_value = 6,
        )''').strip()
        assert_template(result, expected)

    def test_wrong_type(self):
        with pytest.raises(ValueError) as error:
            templates.graphene_scalar('attr', 'wrong')



    #paramaterize the function
    def test_all_scalar_types(self, object_list, attribute):
            #attribute is arbitrary and could be anything
            expected = [
                f'{attribute} = graphene.String()',
                f'{attribute} = graphene.Int()',
                f'{attribute} = graphene.Float()',
                f'{attribute} = graphene.Boolean()',
                f'{attribute} = graphene.types.datetime.Date()',
                f'{attribute} = graphene.types.datetime.DateTime()',
                f'{attribute} = graphene.types.datetime.Time()',
                f'{attribute} = graphene.types.json.JSONString()'
            ]
            for index, type_ in enumerate(object_list):
                assert templates.graphene_scalar(attribute, type_) == expected[index]

#paramaterize the function
def test_graphene_list(object_list, attribute):
    expected = [
        f'{attribute} = graphene.List(graphene.String,)',
        f'{attribute} = graphene.List(graphene.Int,)',
        f'{attribute} = graphene.List(graphene.Float,)',
        f'{attribute} = graphene.List(graphene.Boolean,)',
        f'{attribute} = graphene.List(graphene.types.datetime.Date,)',
        f'{attribute} = graphene.List(graphene.types.datetime.DateTime,)',
        f'{attribute} = graphene.List(graphene.types.datetime.Time,)',
        f'{attribute} = graphene.List(graphene.types.json.JSONString,)'
    ]
    for index, type_ in enumerate(object_list):
        assert templates.graphene_list(attribute, type_) == expected[index]


#paramaterize the function
def test_graphene_field(object_list, attribute):
    expected = [
        f'{attribute} = graphene.Field(graphene.String,)',
        f'{attribute} = graphene.Field(graphene.Int,)',
        f'{attribute} = graphene.Field(graphene.Float,)',
        f'{attribute} = graphene.Field(graphene.Boolean,)',
        f'{attribute} = graphene.Field(graphene.types.datetime.Date,)',
        f'{attribute} = graphene.Field(graphene.types.datetime.DateTime,)',
        f'{attribute} = graphene.Field(graphene.types.datetime.Time,)',
        f'{attribute} = graphene.Field(graphene.types.json.JSONString,)'
    ]
    for index, type_ in enumerate(object_list):
        assert templates.graphene_field(attribute, type_) == expected[index]


# add Tests for ObjectTypes
