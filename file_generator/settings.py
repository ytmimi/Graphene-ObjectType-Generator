import os
from jinja2 import Environment, FileSystemLoader, Template

BASE_DIR =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATE_DIR = os.path.join(BASE_DIR, 'graphene_templates',)

#Jinja2 template environemnt for the project
ENV = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

SCALAR_MAPPING = {
    'string':'graphene.String',
    'int':'graphene.Int',
    'float':'graphene.Float',
    'bool':'graphene.Boolean',
    'id':'graphene.ID',
    'date':'graphene.types.datetime.Date',
    'datetime':'graphene.types.datetime.DateTime',
    'time':'graphene.types.datetime.Time',
    'json':'graphene.types.json.JSONString',
}

def get_graphene_type(type_):
    value = SCALAR_MAPPING.get(type_)
    if value:
        return value
    raise ValueError(
        f'{type_} is not a valid type. '
        f'Please choose one of: {", ".join(SCALAR_MAPPING.keys())}'
    )
