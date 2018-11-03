import json
from templates import graphene_scalar, graphene_list, graphene_field, resolver, objecttype

def _inspect_type(obj):
    '''Returns the name of a Python object:
        ex) an int returns 'int' and a string returns 'str'
    '''
    return type(obj).__name__

def _check_list(attr_name, obj):
    #check taht we don't get back an empty list
    if len(obj) > 0:
        list_type = inspect_type(obj[0])
        if list_type == 'dict':
            #if list_type is a dict then we update list_type before using it in the function
            list_type = f'{attr_name.title()}Type'
        return graphene_list(attr_name, list_type, **kwargs.get(attr_name, {}))
    #else: return a list with an 'UnknownType'
    else:
        return graphene_list(attr_name, 'UnknowType', **kwargs.get(attr_name, {}))

def _check_dict(attr_name, obj):
    return graphene_field(
        attr_name,
        f'{attr_name.title()}Type',
        **kwargs.get(attr_name, {})
    )


def _type_from_obj(attr_name, obj, **kwargs):
    '''
    attr_name: name for the objectType field
    obj: example object that represents the type to expect for the field
    kwargs: a dictionary, where the key is the attr_name passed into the function,
            and the value is a nested dictionary containing the kwargs for the
            render_template function: alt_name, description, required, default_value
    '''
    type_ = inspect_type(obj)
    if type_ == 'list':
        return _check_list()
    elif type_  == 'dict':
        return _check_dict(attr_name)

    else:
        return scalar(attr_name, type_, **kwargs.get(attr_name, {}))


def from_dict(class_name, data_dict={}, **kwargs):
    '''
    class_name: name of the objectType class
    data_dict: usually a dict from a json response
    this will loop through all the keys in a dictionary. If it encounters a nested dict,
    the function will recursivley call itself, and create an objectType class
    for the contents of the inner dict. This will continue until only scalar types are found.
    return: a list
    '''
    fields = []
    resolvers = []
    object_types = []
    def recursive_call(attr_name, value, **kwargs):
        resolvers.append(resolver_func(attr_name))
        new_class_name = f'{attr_name.title()}Type'
        # print(new_class_name, value)
        return objectTypes_from_dict(new_class_name, value, **kwargs.get(new_class_name, {}))

    for attr_name, value in data_dict.items():
        #every attr_name is associated with a field
        fields.append(type_from_obj(attr_name, value, **kwargs))
        #if the field is a dict that means that there are subfield and
        #another objectType should be created
        if inspect_type(value) == 'dict':
            object_types += recursive_call(attr_name, value, **kwargs)
        if inspect_type(value) == 'list' and len(value) > 0 and inspect_type(value[0]) == 'dict':
            object_types += recursive_call(attr_name, value[0], **kwargs)
        elif inspect_type(value) == 'list' and (len(value) == 0 or inspect_type(value[0]) != 'dict'):
            resolvers.append(resolver_func(attr_name))


    object_types.append(create_objectType(class_name, fields, resolvers))
    return object_types


#notes: we need test that include dicts with nested lists
#we need tests that include empty lists
#we need test that include empty dicts


def from_list(attr_name, data_list=[], **kwargs):
    '''
    attr_name: name of the attribute to use in the object type created
    data_list: a list of dictionarys
    this assumes that each dictionary in the list is identical, and will thus only uses the
    first to determin the structure of the sub-objectType
    this will return a list of ObjetType strings, where the first n items spans the dictionary, and the
    last is a Query object with one filed being the attr_name
    return: a list
    '''
    fields = []
    fields.append(type_from_obj(attr_name, data_list, **kwargs))
    resolvers = []
    resolvers.append(resolver_func(attr_name))
    object_types = []
    new_class_name = f'{attr_name.title()}Type'
    #recursively go through the dict looking all objectTypes
    object_types += objectTypes_from_dict(new_class_name, data_list[0], **kwargs)
    object_types.append(create_objectType('Query', fields, resolvers))
    return object_types

def from_json(class_name, json_str, **kwargs):
    '''class_name: name of the class
    url: url to make the request
    url_kwargs: a dict of any kwargs needed to be passed to the request.get()
    kwargs: additional paramerter to pass to the object creation files
    return a list of strings
    '''
    try:
        data = json.loads(json_str)
        if isinstance(data, dict):
            return objectTypes_from_dict(class_name, data, **kwargs)
        if isinstance(data, list):
            attr_name = class_name.lower().replace('type', '')
            return objectTypes_from_list(attr_name, data, **kwargs)
    except Exception as e:
        raise json.JSONDecodeError('Can\'t convert string to a list or dict')
