def imports(*args):
    '''args: properly formated import strings'''
    return '\n'.join(args)

def to_py_file(full_file_name, objecttype, mode='w', imports=None):
    '''
    writes the contents of objectType to a file
    '''
    with open(full_file_name, mode) as f:
        if mode == 'w' and imports:
            f.write(add_imports('import graphene'))
            f.write('\n\n')
        for object in objecttype:
            f.write(object)
            f.write('\n\n')
