from functools import partial
import datetime as dt
from settings import ENV, get_graphene_type

def scalar(attribute_name, type_, alt_name=None,
    description=None, required=False, default_value=None,
    ):
    '''
    All the fields necessary to indicate a graphene scalar type
    '''
    template = ENV.get_template('scalar.txt')
    return template.render(
        attr = attribute_name,
        type = get_graphene_type(type_),
        alt_name = alt_name,
        description = description,
        required = required,
        default_value = default_value
    ).strip()

graphene_string = partial(scalar, type_='string')
graphene_int = partial(scalar, type_='int')
graphene_float = partial(scalar, type_='float')
graphene_bool = partial(scalar, type_='bool')
graphene_id = partial(scalar, type_='id')
graphene_date = partial(scalar, type_='date')
graphene_datetime = partial(scalar, type_='datetime')
graphene_time = partial(scalar, type_='time')
graphene_json = partial(scalar, type_='json')


def graphene_field(attribute_name, type_, alt_name=None,
    description=None, required=False, default_value=None,
    ):
    template = ENV.get_template('field.txt')
    return template.render(

    )

def graphene_list(attribute_name, type_, alt_name=None,
    description=None, required=False, default_value=None,
    ):
    pass

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

def type_from_obj(attr_name, obj, **kwargs):
    '''
    attr_name: name for the objectType field
    obj: example object that represents the type to expect for the field
    kwargs: other kwargs that the graphene_{scalar} functions take
    '''
    if isinstance(obj, str):
        return graphene_string(attribute_name=attr_name, **kwargs)
    elif isinstance(obj, bool):
        return graphene_bool(attribute_name=attr_name, **kwargs)
    elif isinstance(obj, int):
        return graphene_int(attribute_name=attr_name, **kwargs)
    elif isinstance(obj, float):
        return graphene_float(attribute_name=attr_name, **kwargs)
    elif isinstance(obj, dt.datetime):
        return graphene_datetime(attribute_name=attr_name, **kwargs)
    elif isinstance(obj, dt.date):
        return graphene_date(attribute_name=attr_name, **kwargs)
    elif isinstance(obj, dt.time):
        return graphene_time(attribute_name=attr_name, **kwargs)
