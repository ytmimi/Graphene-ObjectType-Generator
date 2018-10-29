from settings import ENV
from scalars import type_from_obj

def create_objectType(class_name, fields=None):
    template = ENV.get_template('graphene_objectType.txt')
    return template.render(class_name=class_name, fields=fields).strip()

def objectType_from_dict(class_name, data_dict):
    '''
    class_name: name of the objectType class
    data_dict: usually a dict from a json response
    '''
    fields = [
        graphene_type_from_obj(attr_name, value)
        for attr_name, value in data_dict.items()
    ]
    return create_objectType(class_name, fields)




if __name__ == '__main__':
    # print(scalar('first', 'string', 'name', 'users first name'))
    print(add_imports('bob', 'hey'))
