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

TYPE_SUFFIX = 'TYPE'
UNKNOWN_TYPE = 'UnknownType'
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
    elif 'Type' in type_:
        return type_
    raise ValueError(
        f'{type_} is not a valid type. '
        f'Please choose one of: {", ".join(GRAPHENE_FIELDS.keys())}. '
        'or supply {filed}Type as the type.'
    )
