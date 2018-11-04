import os
BASE_DIR =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LIVE_TEST = False

GRAPHENE_FIELDS = {
    'str': 'graphene.String',
    'int': 'graphene.Int',
    'float': 'graphene.Float',
    'bool': 'graphene.Boolean',
    'list': 'graphene.List',
    'dict': 'graphene.Field',
    'id': 'graphene.ID',
    'date': 'graphene.types.datetime.Date',
    'datetime': 'graphene.types.datetime.DateTime',
    'time': 'graphene.types.datetime.Time',
    'json': 'graphene.types.json.JSONString',
}

def inspect_type(obj):
    '''Returns the name of a Python object:
        ex) an int returns 'int' and a string returns 'str'
    '''
    return type(obj).__name__

TYPE_SUFFIX = 'Type'
UNKNOWN_TYPE = f'Unknown{TYPE_SUFFIX}'

def class_from_attr(attr_name):
    '''appends the TYPE_SUFFIX to the attr_name passed in'''
    return f'{attr_name.title()}{TYPE_SUFFIX}'

#every where this is encoutered add a description that indicates that the user should
#check the respective API documentation for insight into the field.

def get_graphene_type(type_):
    '''
    Checks to see if the type is in GRAPHENE_FIELDS. If not, a custom type can
    be provided type_ as '{some_filed}Type'
    '''
    value = GRAPHENE_FIELDS.get(type_)
    if value:
        return value
    elif TYPE_SUFFIX in type_:
        return type_
    raise ValueError(f'''
        {type_} is not a valid type.
        Please choose one of: {", ".join(GRAPHENE_FIELDS.keys())}.
        or supply {filed}{TYPE_SUFFIX} as the type.''')
