import os
from functools import partial
from .settings import BASE_DIR, get_graphene_type
from jinja2 import Environment, FileSystemLoader, Template

TEMPLATE_DIR = os.path.join(BASE_DIR, 'graphene_templates',)

ENV = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    lstrip_blocks = True,
)

def _field_types_(attribute_name, type_, alt_name=None,
    description=None, required=False, default_value=None, template=None):
    '''Base function for graphene scalar, list, and filed templates'''
    if template:
        template = ENV.get_template(template)
        return template.render(
            attr = attribute_name,
            type = get_graphene_type(type_),
            alt_name = alt_name,
            description = description,
            required = required,
            default_value = default_value
        )
    raise ValueError('Must designate a template')

graphene_scalar = partial(_field_types_, template='scalar.txt')
graphene_list = partial(_field_types_, template='list.txt')
graphene_field = partial(_field_types_, template='field.txt')

def resolver(attr_name):
    template = Template((
    'def resolve_{{attribute_name}}(self, info, *args, **kwargs):\n'
    '    pass'
    ))
    return template.render(attribute_name=attr_name)

def objecttype(class_name, fields=None, resolvers=None):
    '''
    class_name: name of the class that will be created
    fields: a list of formated strings representing graphene scalars, lists, and field types
    resolvers: a list of formated strings, representing resolver functions
    '''
    template = ENV.get_template('ObjectType.txt')
    return template.render(
        class_name=class_name,
        fields=fields,
        resolvers=resolvers,
        )
